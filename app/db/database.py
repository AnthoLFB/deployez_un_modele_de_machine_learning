import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv("configuration/.env")

try:
    # Récupération de la configuration de la basse de données
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PWD")

    # Création de l'URL de connexion
    SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    # Création du moteur SQLAlchemy (ORM)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"client_encoding": "utf8"})

    # Création / Ouverture de la session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Base pour les modèles SQLAlchemy
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

except:
  print("Une erreur est survenue lors de la récupération des informations de connexion à la base.")