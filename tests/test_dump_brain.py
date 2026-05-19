import os
import pytest
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
