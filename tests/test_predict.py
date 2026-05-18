import pytest
from app.db.models import TrainingDataset

@pytest.fixture
def trained_model(client, db_session, clean_model):
    # Ajouter des données pour l'entraînement
    for i in range(10):
        db_session.add(TrainingDataset(
            revenu_mensuel=3000.0 + i * 100,
            departement="Ventes",
            poste="Commercial",
            nb_experiences_precedentes=i % 3,
            annees_experience_totale=i + 2,
            annees_dans_entreprise=i,
            annees_poste_actuel=i % 5,
            age=20 + i,
            satisfaction_environnement=3,
            note_evaluation_precedente=3.0,
            niveau_hierarchique=1,
            satisfaction_travail=3,
            satisfaction_equipe=3,
            satisfaction_equilibre_pro_perso=3,
            nombre_evaluations=1,
            note_evaluation_actuelle=3.0,
            heures_supplementaires=False,
            augmentation_salaire_precedente=2.0,
            a_quitte_entreprise=(i % 2 == 0),
            nb_participations_pee=1,
            nb_formations_suivies=1,
            code_sondage="S001",
            niveau_education="Bac",
            domaine_etude="Commerce",
            frequence_deplacement="Rare",
            annees_depuis_derniere_promotion=1,
            annees_avec_responsable_actuel=1,
            tranche_distance_domicile_travail="<5km"
        ))
    db_session.commit()
    client.post("/train")

def test_predict_no_model(client, clean_model):
    payload = {
        "revenu_mensuel": 5000.0,
        "departement": "R&D",
        "poste": "Ingénieur",
        "nb_experiences_precedentes": 2,
        "annees_experience_totale": 10,
        "annees_dans_entreprise": 5,
        "annees_poste_actuel": 3,
        "age": 35,
        "satisfaction_environnement": 4,
        "note_evaluation_precedente": 3.5,
        "niveau_hierarchique": 2,
        "satisfaction_travail": 4,
        "satisfaction_equipe": 4,
        "satisfaction_equilibre_pro_perso": 3,
        "nombre_evaluations": 2,
        "note_evaluation_actuelle": 4.0,
        "heures_supplementaires": False,
        "augmentation_salaire_precedente": 5.0,
        "nb_participations_pee": 1,
        "nb_formations_suivies": 2,
        "code_sondage": "S001",
        "niveau_education": "Master",
        "domaine_etude": "Informatique",
        "frequence_deplacement": "Rare",
        "annees_depuis_derniere_promotion": 2,
        "annees_avec_responsable_actuel": 3,
        "tranche_distance_domicile_travail": "10-20km"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 404
    assert "Modèle non trouvé" in response.json()["detail"]

def test_predict_invalid_data(client, trained_model):
    payload = {"age": "vieux"} # Invalide (doit être int)
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_predict_success(client, db_session, trained_model):
    payload = {
        "revenu_mensuel": 5000.0,
        "departement": "R&D",
        "poste": "Ingénieur",
        "nb_experiences_precedentes": 2,
        "annees_experience_totale": 10,
        "annees_dans_entreprise": 5,
        "annees_poste_actuel": 3,
        "age": 35,
        "satisfaction_environnement": 4,
        "note_evaluation_precedente": 3.5,
        "niveau_hierarchique": 2,
        "satisfaction_travail": 4,
        "satisfaction_equipe": 4,
        "satisfaction_equilibre_pro_perso": 3,
        "nombre_evaluations": 2,
        "note_evaluation_actuelle": 4.0,
        "heures_supplementaires": False,
        "augmentation_salaire_precedente": 5.0,
        "nb_participations_pee": 1,
        "nb_formations_suivies": 2,
        "code_sondage": "S001",
        "niveau_education": "Master",
        "domaine_etude": "Informatique",
        "frequence_deplacement": "Rare",
        "annees_depuis_derniere_promotion": 2,
        "annees_avec_responsable_actuel": 3,
        "tranche_distance_domicile_travail": "10-20km"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], bool)
    
    # Vérifier l'insertion en base
    from app.db.models import PredictionResult
    db_predictions = db_session.query(PredictionResult).all()
    assert len(db_predictions) > 0
