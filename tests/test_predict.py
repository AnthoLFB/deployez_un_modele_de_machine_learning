import pytest
from app.db.models import TrainingDataset


# Fixture pour obtenir un modèle entraîné prêt pour les tests de prédiction
@pytest.fixture
def trained_model(client, db_session, clean_model):

    # Ajouter des données pour l'entraînement
    for i in range(10):
        db_session.add(
            TrainingDataset(
                revenu_mensuel=3000.0 + i * 100,
                departement="Ventes",
                poste="Commercial",
                nombre_experiences_precedentes=i % 3,
                annee_experience_totale=i + 2,
                annees_dans_l_entreprise=i,
                annees_dans_le_poste_actuel=i % 5,
                age_rh=str(20 + i),
                satisfaction_employee_environnement=3,
                note_evaluation_precedente=3.0,
                niveau_hierarchique_poste=1,
                satisfaction_employee_nature_travail=3,
                satisfaction_employee_equipe=3,
                satisfaction_employee_equilibre_pro_perso=3,
                note_evaluation_actuelle=3.0,
                heure_supplementaires="Non",
                augementation_salaire_precedente="2%",
                a_quitte_l_entreprise=(i % 2 == 0),
                nombre_participation_pee=1,
                nb_formations_suivies=1,
                niveau_education="Bac",
                domaine_etude="Commerce",
                frequence_deplacement="Rare",
                annees_depuis_la_derniere_promotion=1,
                annes_sous_responsable_actuel=1,
                tranche_distance_domicile_travail="<5km",
            )
        )
    db_session.commit()
    client.post("/train")


def test_predict_no_model(client, clean_model):

    # Vérifie que la prédiction échoue si aucun modèle n'est chargé
    payload = {
        "revenu_mensuel": 5000.0,
        "departement": "R&D",
        "poste": "Ingénieur",
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3,
        "age_rh": "35",
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3.5,
        "niveau_hierarchique_poste": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4.0,
        "heure_supplementaires": "Non",
        "augementation_salaire_precedente": "5%",
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "niveau_education": "Master",
        "domaine_etude": "Informatique",
        "frequence_deplacement": "Rare",
        "annees_depuis_la_derniere_promotion": 2,
        "annes_sous_responsable_actuel": 3,
        "tranche_distance_domicile_travail": "10-20km",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 404
    assert "Modèle non trouvé" in response.json()["detail"]


# Vérifie que la validation des données d'entrée fonctionne via Pydantic
def test_predict_invalid_data(client, trained_model):

    payload = {
        "age_rh": 35
    }  # Invalide (doit être str d'après le schéma, ou du moins on teste l'erreur)
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Pydantic validation error


# Vérifie que la prédiction unitaire fonctionne avec des données valides
def test_predict_success(client, db_session, trained_model):

    payload = {
        "revenu_mensuel": 5000.0,
        "departement": "R&D",
        "poste": "Ingénieur",
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3,
        "age_rh": "35",
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3.5,
        "niveau_hierarchique_poste": 2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4.0,
        "heure_supplementaires": "Non",
        "augementation_salaire_precedente": "5%",
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "niveau_education": "Master",
        "domaine_etude": "Informatique",
        "frequence_deplacement": "Rare",
        "annees_depuis_la_derniere_promotion": 2,
        "annes_sous_responsable_actuel": 3,
        "tranche_distance_domicile_travail": "10-20km",
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
