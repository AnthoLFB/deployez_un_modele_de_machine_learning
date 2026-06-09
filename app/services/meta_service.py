# imports
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv("configuration/.env")


# Permet de voir si l'API est accessible
def get_health_status():
    return {
        "status": "ok",
        "service": os.getenv("APP_NAME", "Déployez un modele de machine learning"),
    }


# Permet d'afficher un message de bienvenu à l'utilisateur, ainsi qu'un guide des routes disponibles.
def display_welcome_message():
    return {
        "message": f"Bonjour, bienvenue sur l'application : {os.getenv('APP_NAME', 'Déployez un modele de machine learning')}",
        "routes": {
            "health": {"description": "Vérifier l'état de l'API", "path": "/health"},
            "train": {
                "description": "Entraîner le modèle avec un dataset d'entraînement",
                "path": "/train",
            },
            "dump_brain": {
                "description": "Supprimer la mémoire du modèle pour ré-entraîner",
                "path": "/dump-brain",
            },
            "predict": {"description": "Prédire un résultat", "path": "/predict"},
            "predict_csv": {
                "description": "Prédire une liste de résultats",
                "path": "/predict-csv",
            },
            "show_list": {
                "description": "Afficher les résultats déjà prédits",
                "path": "/show-list",
            },
            "docs": {
                "description": "Afficher la documentation swagger",
                "path": "/docs",
            },
        },
    }
