from app.db.models import PredictionResult, InputData


# Vérifie que la liste des prédictions est vide au démarrage
def test_show_list_empty(client):

    response = client.get("/show-list")
    assert response.status_code == 200
    assert response.json() == []


# Vérifie que les prédictions enregistrées sont correctement retournées par /show-list
def test_show_list_with_data(client, db_session):

    # Ajouter une donnée d'entrée et une prédiction associée
    input_data = InputData(
        revenu_mensuel=5000.0,
        departement="R&D",
        poste="Ingénieur",
        nombre_experiences_precedentes=2,
        annee_experience_totale=10,
        annees_dans_l_entreprise=5,
        annees_dans_le_poste_actuel=3,
        age_rh="35",
        satisfaction_employee_environnement=4,
        note_evaluation_precedente=3.5,
        niveau_hierarchique_poste=2,
        satisfaction_employee_nature_travail=4,
        satisfaction_employee_equipe=4,
        satisfaction_employee_equilibre_pro_perso=3,
        note_evaluation_actuelle=4.0,
        heure_supplementaires="Non",
        augementation_salaire_precedente="5.0",
        nombre_participation_pee=1,
        nb_formations_suivies=2,
        niveau_education="Master",
        domaine_etude="Informatique",
        frequence_deplacement="Rare",
        annees_depuis_la_derniere_promotion=2,
        annes_sous_responsable_actuel=3,
        tranche_distance_domicile_travail="10-20km",
    )
    db_session.add(input_data)
    db_session.commit()
    db_session.refresh(input_data)

    prediction = PredictionResult(input_id=input_data.id, prediction=True)
    db_session.add(prediction)
    db_session.commit()

    response = client.get("/show-list")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["prediction"] is True
