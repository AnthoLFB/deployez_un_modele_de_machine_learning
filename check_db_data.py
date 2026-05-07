import sys
import os

# Ajouter le dossier parent au path pour importer 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import TrainingDataset

def debug_check_data():
    print("Vérification des données d'entraînement...")
    db = SessionLocal()
    try:
        data = db.query(TrainingDataset).all()
        print(f"Nombre d'enregistrements trouvés : {len(data)}")
        for i, row in enumerate(data[:5]):
            print(f"Ligne {i+1}: age={row.age}, salary={row.salary}, target={row.target}")
        
        if len(data) == 0:
            print("AVERTISSEMENT : La table 'training_dataset' est VIDE.")
            print("Veuillez exécuter 'python seed_db.py' pour ajouter des données.")
    except Exception as e:
        print(f"Erreur lors de la lecture de la base : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_check_data()
