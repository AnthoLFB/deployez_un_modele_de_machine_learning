import io
import pytest
import pandas as pd
from app.db.models import TrainingDataset

 # Fixture pour obtenir un modèle entraîné prêt pour les tests de prédiction CSV
@pytest.fixture
def trained_model(client, db_session, clean_model):

    for i in range(10):
        db_session.add(TrainingDataset(
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
            augementation_salaire_precedente="2.0",
            a_quitte_l_entreprise=(i % 2 == 0),
            nombre_participation_pee=1,
            nb_formations_suivies=1,
            niveau_education="Bac",
            domaine_etude="Commerce",
            frequence_deplacement="Rare",
            annees_depuis_la_derniere_promotion=1,
            annes_sous_responsable_actuel=1,
            tranche_distance_domicile_travail="<5km"
        ))
    db_session.commit()
    client.post("/train")

# Vérifie que la prédiction par lot (CSV) fonctionne correctement
def test_predict_csv_success(client, trained_model):

    data = {
        "revenu_mensuel": [5000.0, 6000.0],
        "departement": ["R&D", "Sales"],
        "poste": ["Ingénieur", "Manager"],
        "nombre_experiences_precedentes": [2, 3],
        "annee_experience_totale": [10, 15],
        "annees_dans_l_entreprise": [5, 8],
        "annees_dans_le_poste_actuel": [3, 4],
        "age_rh": ["35", "40"],
        "satisfaction_employee_environnement": [4, 3],
        "note_evaluation_precedente": [3.5, 4.0],
        "niveau_hierarchique_poste": [2, 3],
        "satisfaction_employee_nature_travail": [4, 4],
        "satisfaction_employee_equipe": [4, 4],
        "satisfaction_employee_equilibre_pro_perso": [3, 3],
        "note_evaluation_actuelle": [4.0, 4.0],
        "heure_supplementaires": ["Non", "Oui"],
        "augementation_salaire_precedente": ["5%", "6%"],
        "nombre_participation_pee": [1, 1],
        "nb_formations_suivies": [2, 2],
        "niveau_education": ["Master", "Bachelor"],
        "domaine_etude": ["Informatique", "Business"],
        "frequence_deplacement": ["Rare", "Frequent"],
        "annees_depuis_la_derniere_promotion": [2, 3],
        "annes_sous_responsable_actuel": [3, 4],
        "tranche_distance_domicile_travail": ["10-20km", "0-5km"]
    }
    df = pd.DataFrame(data)
    stream = io.BytesIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    response = client.post(
        "/predict-csv",
        files={"file": ("test.csv", stream, "text/csv")}
    )
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert len(response.json()["predictions"]) == 2

# Vérifie que l'API rejette les fichiers qui ne sont pas au format CSV
def test_predict_csv_invalid_format(client):

    response = client.post(
        "/predict-csv",
        files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")}
    )
    assert response.status_code == 400
    assert "Le fichier doit être au format CSV" in response.json()["detail"]

# Vérifie le comportement lors de l'envoi d'un fichier CSV vide
def test_predict_csv_empty(client, trained_model):

    stream = io.BytesIO(b"")
    response = client.post(
        "/predict-csv",
        files={"file": ("empty.csv", stream, "text/csv")}
    )
    assert response.status_code == 400

# Vérifie que la prédiction CSV échoue si aucun modèle n'est présent
def test_predict_csv_no_model(client, clean_model):

    data = {"age": [25]}
    df = pd.DataFrame(data)
    stream = io.BytesIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
    
    response = client.post(
        "/predict-csv",
        files={"file": ("test.csv", stream, "text/csv")}
    )
    assert response.status_code == 400 or response.status_code == 404

# Vérifie le comportement lors de l'envoi d'un CSV avec des colonnes manquantes
def test_predict_csv_missing_columns(client, trained_model):

    data = {"age": [25]} # Colonnes manquantes pour le modèle
    df = pd.DataFrame(data)
    stream = io.BytesIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
    
    response = client.post(
        "/predict-csv",
        files={"file": ("test.csv", stream, "text/csv")}
    )
    assert response.status_code == 400
    assert "Erreur lors de la prédiction" in response.json()["detail"]
