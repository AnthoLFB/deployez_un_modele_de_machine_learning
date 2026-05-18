import os
from app.db.models import TrainingDataset

def test_train_no_data(client, clean_model):
    # Tester l'entraînement quand il n'y a pas de données
    response = client.post("/train")
    assert response.status_code == 500
    assert "Aucune donnée d'entraînement trouvée" in response.json()["detail"]

def test_train_success(client, db_session, clean_model):
    # Ajouter des données de test
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

    # Premier entraînement
    response = client.post("/train")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert os.path.exists("model.pkl")

    # Tentative de ré-entraînement sans force
    response = client.post("/train")
    assert response.status_code == 409
    assert "Le modèle existe déjà" in response.json()["detail"]

    # Ré-entraînement avec force
    response = client.post("/train?force=true")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
