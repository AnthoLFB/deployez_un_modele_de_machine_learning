import pytest
import pandas as pd
from app.services.trainer import Trainer
from sklearn.ensemble import RandomForestClassifier

# Vérifie la création et l'entraînement d'un pipeline simple (sans optimisation)
def test_train_model_pipeline_simple():

    X = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': ['A', 'B', 'A', 'B', 'A']
    })
    y = pd.Series([0, 1, 0, 1, 0])
    
    model = RandomForestClassifier(random_state=42)
    pipeline = Trainer.train_model_pipeline(X, y, model)
    
    assert pipeline is not None
    assert hasattr(pipeline, 'predict')
    
    # Test prediction
    pred = pipeline.predict(X)
    assert len(pred) == 5

# Vérifie l'entraînement de la pipeline avec recherche d'hyperparamètres (GridSearchCV)
def test_train_model_pipeline_optimize():

    X = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    })
    y = pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    
    model = RandomForestClassifier(random_state=42)
    param_grid = {'n_estimators': [10, 20]}
    
    pipeline = Trainer.train_model_pipeline(X, y, model, param_grid=param_grid)
    
    assert pipeline is not None

    # Vérifier que c'est le meilleur estimateur issu de GridSearchCV
    assert pipeline.named_steps['classifier'].n_estimators in [10, 20]

def test_train_from_db_no_target(db_session):
    # On mock crud.get_training_data indirectement en n'ajoutant pas de données ou en ajoutant des données sans la colonne target
    # Mais Trainer._to_dict utilise les colonnes de la table models.TrainingDataset
    # Donc on va mocker crud.get_training_data
    pass

class MockData:
    def __init__(self, data_dict):
        self.__dict__.update(data_dict)
        # Mock de la structure de la table SQLAlchemy pour la fonction _to_dict
        class Column:
            def __init__(self, name):
                self.name = name
        
        class Table:
            def __init__(self, columns):
                self.columns = [Column(c) for c in columns]
        
        self.__table__ = Table(list(data_dict.keys()))

# Vérifie la conversion d'un objet SQLAlchemy en dictionnaire pour le Trainer
def test_trainer_to_dict():

    data = {'id': 1, 'name': 'test'}
    obj = MockData(data)
    result = Trainer._to_dict(obj)
    assert result == data

# Vérifie la gestion d'erreur quand une colonne obligatoire est manquante en base
def test_train_from_db_error_handling(db_session, monkeypatch):

    # Mock crud.get_training_data pour retourner des données sans la cible
    def mock_get_training_data(db):
        return [MockData({'id': 1, 'feature': 10})]
    
    import app.db.crud as crud
    monkeypatch.setattr(crud, "get_training_data", mock_get_training_data)
    
    result = Trainer.train_from_db(db_session)
    assert result["status"] == "error"
    assert "La colonne target 'a_quitte_l_entreprise' est absente" in result["message"]

# Vérifie la gestion des exceptions lors de la récupération des données en base
def test_train_from_db_exception(db_session, monkeypatch):

    def mock_get_training_data(db):
        raise Exception("DB Error")
    
    import app.db.crud as crud
    monkeypatch.setattr(crud, "get_training_data", mock_get_training_data)
    
    result = Trainer.train_from_db(db_session)
    assert result["status"] == "error"
    assert "Erreur lors de l'entraînement : DB Error" in result["message"]
