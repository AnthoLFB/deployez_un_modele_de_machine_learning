import sys
import os

# Ajouter le dossier parent au path pour importer 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine, Base
from app.db.models import TrainingDataset

def seed_data():
    print("Création des tables (si nécessaire)...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        count = db.query(TrainingDataset).count()
        if count > 0:
            print(f"La table training_dataset contient déjà {count} enregistrements. Saut du peuplement.")
            return

        print("Ajout de données d'entraînement factices...")
        dummy_data = [
            TrainingDataset(age=25, salary=2000, target=0),
            TrainingDataset(age=35, salary=3500, target=1),
            TrainingDataset(age=45, salary=5000, target=1),
            TrainingDataset(age=20, salary=1500, target=0),
            TrainingDataset(age=50, salary=6000, target=1),
            TrainingDataset(age=30, salary=2800, target=0),
            TrainingDataset(age=40, salary=4200, target=1),
            TrainingDataset(age=28, salary=2200, target=0),
        ]
        
        db.add_all(dummy_data)
        db.commit()
        print("Données ajoutées avec succès !")
    except Exception as e:
        print(f"Erreur lors du peuplement : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
