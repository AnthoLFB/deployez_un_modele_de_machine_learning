import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv("configuration/.env")

try:
    # Récupération de l'environnement
    app_env = os.getenv("APP_ENV", "staging").lower()

    # En fonction de l'env, on travaille en BDD de test ou de production.
    if app_env == "production":
        host = os.getenv("DB_PRODUCTION_HOST")
        port = os.getenv("DB_PRODUCTION_PORT")
        dbname = os.getenv("DB_PRODUCTION_NAME")
        user = os.getenv("DB_PRODUCTION_USER")
        password = os.getenv("DB_PRODUCTION_PWD")
    else:
        # Par défaut on utilise le staging
        host = os.getenv("DB_STAGING_HOST")
        port = os.getenv("DB_STAGING_PORT")
        dbname = os.getenv("DB_STAGING_NAME")
        user = os.getenv("DB_STAGING_USER")
        password = os.getenv("DB_STAGING_PWD")

    # Création de l'URL de connexion
    SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    # Création du moteur SQLAlchemy (ORM)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"client_encoding": "utf8"}
    )

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

except Exception as e:
    print(
        f"Une erreur est survenue lors de la récupération des informations de connexion à la base : {e}"
    )
