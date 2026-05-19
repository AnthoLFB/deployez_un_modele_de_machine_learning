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
        nb_experiences_precedentes=2,
        annees_experience_totale=10,
        annees_dans_entreprise=5,
        annees_poste_actuel=3,
        age=35,
        satisfaction_environnement=4,
        note_evaluation_precedente=3.5,
        niveau_hierarchique=2,
        satisfaction_travail=4,
        satisfaction_equipe=4,
        satisfaction_equilibre_pro_perso=3,
        nombre_evaluations=2,
        note_evaluation_actuelle=4.0,
        heures_supplementaires=False,
        augmentation_salaire_precedente=5.0,
        nb_participations_pee=1,
        nb_formations_suivies=2,
        code_sondage="S001",
        niveau_education="Master",
        domaine_etude="Informatique",
        frequence_deplacement="Rare",
        annees_depuis_derniere_promotion=2,
        annees_avec_responsable_actuel=3,
        tranche_distance_domicile_travail="10-20km"
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
