import joblib
import os
import shutil
from datetime import datetime

MODEL_PATH = "model.pkl"
HISTORY_DIR = "storage/history"

class ModelManager:
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
            if not os.path.exists(HISTORY_DIR):
                os.makedirs(HISTORY_DIR)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = os.path.join(HISTORY_DIR, f"model_{timestamp}.pkl")
            
            # Déplacer le modèle vers l'historique
            shutil.move(MODEL_PATH, archive_path)
            return archive_path
        return None

    @staticmethod
    def model_exists():
        """Vérifie si le modèle existe."""
        return os.path.exists(MODEL_PATH)
