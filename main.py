# Imports
import os
from dotenv import load_dotenv

# Récupération des variables d'environnement
load_dotenv("configuration/.env")


# Initialisation du programme
def main():
    print(f"Bonjour ! Bienvenue sur le projet : {os.getenv('APP_NAME')}")


if __name__ == "__main__":
    main()
