import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sqlalchemy.orm import Session
from ..db import crud, models

class Trainer:

    DEFAULT_PARAM_GRID = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [None, 6, 8, 10, 12, 20],
        'min_samples_split': [2, 5]
    }

    @staticmethod
    def train_model_pipeline(X, y, model, param_grid=None, scoring="f1"):
        """
        Crée et entraîne une pipeline sklearn avec prétraitement automatique.
        """
        # Identification des types de colonnes
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()

        print(f"Info: Features numériques: {numeric_features}")
        print(f"Info: Features catégorielles: {categorical_features}")

        # Prétraitement
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )

        # Création de la pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])

        if param_grid:
            print(f"Info: Lancement de GridSearchCV avec scoring={scoring}...")
            # On adapte le param_grid pour la pipeline (ajout du préfixe 'classifier__')
            pipeline_param_grid = {f'classifier__{k}': v for k, v in param_grid.items()}
            
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            grid_search = GridSearchCV(pipeline, pipeline_param_grid, cv=cv, scoring=scoring, n_jobs=-1)
            grid_search.fit(X, y)

            print(f"Best params: {grid_search.best_params_}")
            print(f"Best score ({scoring}): {grid_search.best_score_:.4f}")
            
            return grid_search.best_estimator_
        else:
            print("Info: Entraînement simple de la pipeline...")
            pipeline.fit(X, y)
            return pipeline

    @staticmethod
    def train_from_db(db: Session, param_grid=None, optimize=False):
        """Récupère les données de la DB et entraîne le modèle."""

        try:
            # On récupère les données d'entrainement
            data = crud.get_training_data(db)

            # Si on ne récupère pas de données, on déclenche une erreur
            if not data:
                return {
                    "status": "error",
                    "message": f"Aucune donnée d'entraînement trouvée dans la table : '{models.TrainingDataset.__tablename__}'.",
                    "data": None
                }

            # Conversion en DataFrame pandas
            df = pd.DataFrame([Trainer._to_dict(d) for d in data])
            
            # On sépare les features et la target
            if "a_quitte_entreprise" not in df.columns:
                return {
                    "status": "error",
                    "message": "La colonne target 'a_quitte_entreprise' est absente des données.",
                    "data": None
                }

            X = df.drop(columns=["id", "created_at", "a_quitte_entreprise"])
            y = df["a_quitte_entreprise"]

            # Création et entraînement du modèle via la nouvelle fonction
            base_model = RandomForestClassifier(random_state=42)
            
            # Gestion du param_grid par défaut si l'optimisation est demandée
            if optimize and param_grid is None:
                param_grid = Trainer.DEFAULT_PARAM_GRID
                print("Info: Utilisation du param_grid par défaut pour l'optimisation.")

            trained_pipeline = Trainer.train_model_pipeline(X, y, base_model, param_grid=param_grid)

            # Si l'entrainement c'est bien passé on return un succès
            return {
                "status": "success",
                "message": "Modèle entraîné avec succès via pipeline.",
                "data": trained_pipeline
            }

        except Exception as e:
            error_msg = f"Erreur lors de l'entraînement : {str(e)}"
            print(f"ERROR: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "data": None
            }

    @staticmethod
    def _to_dict(obj):
        """Helper pour convertir une ligne SQLAlchemy en dict pour sklearn."""
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
