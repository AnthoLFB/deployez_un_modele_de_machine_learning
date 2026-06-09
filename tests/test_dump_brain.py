import os
from app.db.models import TrainingDataset


# Vérifie le comportement de l'archivage lorsqu'aucun modèle n'est présent
def test_dump_brain_no_model(client, clean_model):

    response = client.post("/dump-brain")
    assert response.status_code == 200
    assert response.json()["status"] == "not_found"


# Vérifie que l'archivage du modèle fonctionne correctement
def test_dump_brain_success(client, db_session, clean_model):

    # Entraîner un modèle d'abord
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
                augementation_salaire_precedente="2.0",
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
    assert os.path.exists("model.pkl")

    # Archiver
    response = client.post("/dump-brain")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert not os.path.exists("model.pkl")

    # Vérifier que le fichier est dans l'historique
    archive_path = response.json()["data"]["archive_path"]
    assert os.path.exists(archive_path)

    # Nettoyage de l'archive créée
    if os.path.exists(archive_path):
        os.remove(archive_path)
