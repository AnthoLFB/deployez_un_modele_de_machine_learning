#Imports
import os
import joblib
import shutil
from datetime import datetime
from dotenv import load_dotenv
from .trainer import Trainer

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv("configuration/.env")

# Définition des noms et emplacements de stockage des fichiers PKL
MODEL_PATH = os.getenv("MODEL_BASE_FILENAME", "model.pkl")
MODEL_STORAGE = os.getenv("MODEL_BASE_STORAGE_PATH", "storage/history")
MODEL_HISTORY_STORAGE = os.getenv("MODEL_HISTORY_STORAGE_PATH", "storage/history")

class ModelManager:

    def train(force, db, param_grid=None, optimize=False):
        """Orchestre l'entraînement du modèle."""
        try:
            # On vérifie le status du modèle
            if ModelManager.model_exists() and not force:
                return {
                    "status": "conflict",
                    "message": "Le modèle existe déjà. Utilisez force=true pour ré-entraîner."
                }

            # Le modèle existe et l'utilisateur souhaite forcer le ré-entrainement
            if ModelManager.model_exists() and force:
                # On historise l'ancienne mémoire du modèle
                ModelManager.archive_model()

            # On lance l'entrainement du modèle via le Trainer
            result = Trainer.train_from_db(db, param_grid=param_grid, optimize=optimize)

            if result["status"] == "success":
                # Sauvegarde via le manager
                print("Info: Sauvegarde du modèle...")
                ModelManager.save_model(result["data"])
                print("Info: Sauvegarde réussie...")
                
                return {
                    "status": "success",
                    "message": result["message"]
                }
            else:
                return {
                    "status": "error",
                    "message": result["message"]
                }

        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                "status": "error",
                "message": f"Erreur interne lors de l'entraînement : {str(e)}"
            }

    @staticmethod
    def save_model(model):
        """Sauvegarde le modèle actif."""
        joblib.dump(model, MODEL_PATH)

    @staticmethod
    def load_model():
        """Charge le modèle actif s'il existe."""
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
        return None

    @staticmethod
    def archive_model():
        """Archive le modèle actuel dans l'historique."""
        if os.path.exists(MODEL_PATH):
            if not os.path.exists(MODEL_HISTORY_STORAGE):
                os.makedirs(MODEL_HISTORY_STORAGE)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = os.path.join(MODEL_HISTORY_STORAGE, f"model_{timestamp}.pkl")
            
            # Déplacer le modèle vers l'historique
            shutil.move(MODEL_PATH, archive_path)
            return {
                "status": "success",
                "message": f"Modèle archivé avec succès vers {archive_path}",
                "data": {"archive_path": archive_path}
            }
        return {
            "status": "not_found",
            "message": "Aucun modèle à archiver.",
            "data": None
        }

    @staticmethod
    def model_exists():
        """Vérifie si le modèle existe."""
        return os.path.exists(MODEL_PATH)
