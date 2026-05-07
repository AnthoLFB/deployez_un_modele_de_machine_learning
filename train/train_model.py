import sys
import os

# Ajouter le dossier parent au path pour importer 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.services.trainer import Trainer

def run_training():
    print("Démarrage de l'entraînement autonome...")
    db = SessionLocal()
    try:
        success, message = Trainer.train_from_db(db)
        print(message)
    finally:
        db.close()

if __name__ == "__main__":
    run_training()
