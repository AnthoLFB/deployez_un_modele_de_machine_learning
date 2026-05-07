import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy.orm import Session
from ..db import crud, models
from .model_manager import ModelManager

class Trainer:
    @staticmethod
    def train_from_db(db: Session):
        """Récupère les données de la DB et entraîne le modèle."""
        try:
            data = crud.get_training_data(db)
            
            print(f"DEBUG: Nombre de lignes récupérées pour l'entraînement : {len(data)}")
            
            if not data:
                return False, f"Aucune donnée d'entraînement trouvée dans la table '{models.TrainingDataset.__tablename__}'."

            # Conversion en DataFrame pandas
            print("DEBUG: Conversion des données en DataFrame...")
            df = pd.DataFrame([{"age": d.age, "salary": d.salary, "target": d.target} for d in data])
            print(f"DEBUG: Aperçu du DataFrame :\n{df.head()}")
            
            X = df[["age", "salary"]]
            y = df["target"]

            # Création et entraînement du modèle
            print("DEBUG: Entraînement du RandomForest...")
            model = RandomForestClassifier(n_estimators=100)
            model.fit(X, y)

            # Sauvegarde via le manager
            print("DEBUG: Sauvegarde du modèle...")
            ModelManager.save_model(model)
            
            return True, "Modèle entraîné et sauvegardé avec succès."
        except Exception as e:
            error_msg = f"Erreur lors de l'entraînement : {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, error_msg
