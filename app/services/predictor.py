import logging
import traceback
from sqlalchemy.orm import Session
from ..db import crud
from .model_manager import ModelManager
import pandas as pd

logger = logging.getLogger(__name__)


class Predictor:
    @staticmethod
    def predict(db: Session, input_data: dict):
        """Effectue une prédiction unitaire."""
        try:
            # 1. Enregistrer les données dans inputs
            input_record = crud.create_input(db, input_data)

            # 2. Charger le modèle
            model = ModelManager.load_model()
            if model is None:
                return {
                    "status": "not_found",
                    "message": "Modèle non trouvé. Veuillez entraîner le modèle d'abord.",
                    "data": None,
                }

            # 3. Faire la prédiction
            df_input = pd.DataFrame([input_data])

            # Avec la pipeline, plus besoin de get_dummies ou de reindex manuel
            prediction_val = bool(model.predict(df_input)[0])

            # 4. Enregistrer le résultat dans predictions
            prediction_record = crud.create_prediction(
                db, input_record.id, prediction_val
            )

            # 5. Logger l'interaction
            model_output = {"prediction": prediction_val}
            crud.create_interaction_log(
                db,
                input_record.id,
                prediction_record.id,
                input_data,
                model_output,
                "success",
            )

            return {
                "status": "success",
                "message": "Prédiction effectuée avec succès.",
                "data": {"prediction": prediction_val},
            }
        except Exception as e:
            error_msg = f"Erreur lors de la prédiction : {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return {"status": "error", "message": error_msg, "data": None}

    @staticmethod
    def predict_batch(db: Session, df: pd.DataFrame):
        """Effectue des prédictions en masse à partir d'un DataFrame."""
        try:
            # 1. Charger le modèle
            model = ModelManager.load_model()
            if model is None:
                return {
                    "status": "not_found",
                    "message": "Modèle non trouvé. Veuillez entraîner le modèle d'abord.",
                    "data": None,
                }

            # 2. Préparation pour la prédiction
            df_records = df.copy()

            # Avec la pipeline, plus besoin de get_dummies ou de reindex manuel
            # 3. Prédiction
            predictions = model.predict(df)

            results = []
            # 4. Enregistrement en base de données pour chaque ligne
            for i, row in df_records.iterrows():
                row_dict = row.to_dict()
                prediction_val = bool(predictions[i])

                input_record = crud.create_input(db, row_dict)
                prediction_record = crud.create_prediction(
                    db, input_record.id, prediction_val
                )
                crud.create_interaction_log(
                    db,
                    input_record.id,
                    prediction_record.id,
                    row_dict,
                    {"prediction": prediction_val},
                    "success",
                )

                results.append({"id": i, "prediction": prediction_val})

            return {
                "status": "success",
                "message": f"{len(results)} prédictions effectuées avec succès.",
                "data": results,
            }
        except Exception as e:
            error_msg = f"Erreur lors de la prédiction batch : {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return {"status": "error", "message": error_msg, "data": None}
