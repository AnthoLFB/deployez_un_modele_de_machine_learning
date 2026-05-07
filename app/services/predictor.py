import logging
import traceback
from sqlalchemy.orm import Session
from ..db import crud
from .model_manager import ModelManager
import pandas as pd

logger = logging.getLogger(__name__)

class Predictor:
    @staticmethod
    def predict(db: Session, age: int, salary: float):
        try:
            # 1. Enregistrer les données dans inputs
            input_record = crud.create_input(db, age, salary)
            
            # 2. Charger le modèle
            model = ModelManager.load_model()
            if model is None:
                return None, "Modèle non trouvé. Veuillez entraîner le modèle d'abord."

            # 3. Faire la prédiction
            # Préparation de la donnée pour le modèle
            X = pd.DataFrame([[age, salary]], columns=["age", "salary"])
            prediction_val = int(model.predict(X)[0])

            # 4. Enregistrer le résultat dans predictions
            prediction_record = crud.create_prediction(db, input_record.id, prediction_val)

            # 5. Logger l'interaction
            user_input = {"age": age, "salary": salary}
            model_output = {"prediction": prediction_val}
            crud.create_interaction_log(
                db, 
                input_record.id, 
                prediction_record.id, 
                user_input, 
                model_output, 
                "success"
            )

            return prediction_val, None
        except Exception as e:
            error_msg = f"Erreur lors de la prédiction : {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return None, error_msg
