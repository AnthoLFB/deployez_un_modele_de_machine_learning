from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import crud
from ..schemas.input import PredictionInput
from ..services.model_manager import ModelManager
from ..services.trainer import Trainer
from ..services.predictor import Predictor

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok bobby"}

@router.post("/train")
def train_model(force: bool = False, db: Session = Depends(get_db)):
    if ModelManager.model_exists() and not force:
        return {"message": "Le modèle existe déjà. Utilisez force=true pour réentraîner."}
    
    if force:
        ModelManager.archive_model()
    
    success, message = Trainer.train_from_db(db)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"message": message}

@router.post("/dump-brain")
def dump_brain():
    archive_path = ModelManager.archive_model()
    if archive_path:
        return {"message": f"Modèle archivé avec succès vers {archive_path}"}
    return {"message": "Aucun modèle à archiver."}

@router.post("/predict")
def predict(data: PredictionInput, db: Session = Depends(get_db)):
    prediction, error = Predictor.predict(db, data.age, data.salary)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"prediction": prediction}

@router.get("/show-list")
def show_list(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    predictions = crud.get_predictions(db, skip=offset, limit=limit)
    return predictions
