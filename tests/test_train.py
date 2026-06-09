import os
from app.db.models import TrainingDataset

# Vérifie que l'entraînement échoue lorsqu'aucune donnée n'est présente en base
def test_train_no_data(client, clean_model):

    # Tester l'entraînement quand il n'y a pas de données
    response = client.post("/train")
    assert response.status_code == 500
    assert "Aucune donnée d'entraînement trouvée" in response.json()["detail"]

# Vérifie que l'entraînement du modèle se déroule correctement avec des données valides
def test_train_success(client, db_session, clean_model):

    # Ajouter des données de test
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

 # Vérifie que l'entraînement avec optimisation (GridSearchCV) fonctionne
def test_train_with_optimization(client, db_session, clean_model):

    # Ajouter des données
    for i in range(20): # Plus de données pour CV=5
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
    
    # Entraînement avec optimisation
    response = client.post("/train?optimize=true")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert os.path.exists("model.pkl")

# Vérifie que l'entraînement fonctionne avec une grille de paramètres personnalisée
def test_train_with_param_grid(client, db_session, clean_model):

    # Ajouter des données
    for i in range(15):
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

    response = client.post("/train?optimize=true")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
