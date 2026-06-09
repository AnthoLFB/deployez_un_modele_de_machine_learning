import os
import joblib
from app.services.model_manager import ModelManager


# Vérifie que la sauvegarde et le chargement du modèle fonctionnent correctement
def test_save_load_model(clean_model):

    model = {"name": "test_model"}
    ModelManager.save_model(model)

    assert os.path.exists("model.pkl")

    loaded_model = ModelManager.load_model()
    assert loaded_model == model


# Vérifie que le chargement retourne None si aucun fichier modèle n'existe
def test_load_model_none():

    if os.path.exists("model.pkl"):
        os.remove("model.pkl")
    assert ModelManager.load_model() is None


# Vérifie que l'archivage déplace correctement le fichier modèle vers l'historique
def test_archive_model(clean_model):

    # Créer un modèle à archiver
    model = {"name": "old_model"}
    ModelManager.save_model(model)

    result = ModelManager.archive_model()
    assert result["status"] == "success"
    assert not os.path.exists("model.pkl")

    archive_path = result["data"]["archive_path"]
    assert os.path.exists(archive_path)

    # Vérifier le contenu
    archived_model = joblib.load(archive_path)
    assert archived_model == model

    # Nettoyage de l'archive
    os.remove(archive_path)


# Vérifie le message d'erreur lors de l'archivage si aucun modèle n'est présent
def test_archive_model_not_found():

    if os.path.exists("model.pkl"):
        os.remove("model.pkl")

    result = ModelManager.archive_model()
    assert result["status"] == "not_found"
    assert result["message"] == "Aucun modèle à archiver."


# Vérifie la détection de l'existence du fichier modèle
def test_model_exists(clean_model):

    assert not ModelManager.model_exists()
    ModelManager.save_model({"name": "test"})
    assert ModelManager.model_exists()


# Vérifie la gestion des exceptions lors de l'appel à ModelManager.train
def test_model_manager_train_exception(db_session, monkeypatch):

    def mock_train_from_db(db, param_grid=None, optimize=False):
        raise Exception("Unexpected error")

    from app.services.trainer import Trainer

    monkeypatch.setattr(Trainer, "train_from_db", mock_train_from_db)

    result = ModelManager.train(force=True, db=db_session)
    assert result["status"] == "error"
    assert "Erreur interne lors de l'entraînement" in result["message"]
