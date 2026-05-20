# Imports
import io
import pandas as pd
from ..db import crud
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..services.trainer import Trainer
from typing import Dict, Any, Optional
from ..services.predictor import Predictor
from ..schemas.input import PredictionInput, TrainInput
from ..services.model_manager import ModelManager
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from ..services.meta_service import display_welcome_message, get_health_status

# Création et organisation des routes via FastAPI.
router = APIRouter()

# Route de base (message de bienvenu + liste des routes dispo)
@router.get("/")
def welcome() :
    return display_welcome_message()

# Permte de checker si l'API est accessible
@router.get("/health")
def health_check():
    return get_health_status()

# Permet d'entrainer le modèle
@router.post('/train')
def train_model(
    payload: Optional[TrainInput] = None,
    force: bool = False, 
    optimize: bool = False, 
    db: Session = Depends(get_db)
):
    param_grid = payload.param_grid if payload else None
    result = ModelManager.train(force, db, param_grid=param_grid, optimize=optimize)
    
    if result["status"] == "success":
        return result
    elif result["status"] == "conflict":
        raise HTTPException(status_code=409, detail=result["message"])
    else:
        raise HTTPException(status_code=500, detail=result["message"])

# Permet d'archiver le modèle actuel
@router.post("/dump-brain")
def dump_brain():
    result = ModelManager.archive_model()
    
    if result["status"] == "success":
        return result
    elif result["status"] == "not_found":
        return result
    else:
        raise HTTPException(status_code=500, detail=result["message"])

# Permet de lancer une prédiction sur un seul élément
@router.post("/predict")
def predict(data: PredictionInput, db: Session = Depends(get_db)):
    result = Predictor.predict(db, data.model_dump())
    
    if result["status"] == "success":
        return result["data"]
    elif result["status"] == "not_found":
        raise HTTPException(status_code=404, detail=result["message"])
    else:
        raise HTTPException(status_code=400, detail=result["message"])

# Permet de lancer des prédictions sur un ensemble d'éléments via un fichier CSV
@router.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV.")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        result = Predictor.predict_batch(db, df)
        
        if result["status"] == "success":
            return {"predictions": result["data"]}
        elif result["status"] == "not_found":
            raise HTTPException(status_code=404, detail=result["message"])
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la lecture du CSV : {str(e)}")

# Permet d'afficher une liste de X predictions déjà effectuées
@router.get("/show-list")
def show_list(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    predictions = crud.get_predictions(db, skip=offset, limit=limit)
    return predictions
