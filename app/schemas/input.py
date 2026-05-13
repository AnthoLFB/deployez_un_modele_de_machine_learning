from pydantic import BaseModel
from typing import Optional

class PredictionInput(BaseModel):
    revenu_mensuel: float
    departement: str
    poste: str
    nb_experiences_precedentes: int
    annees_experience_totale: int
    annees_dans_entreprise: int
    annees_poste_actuel: int
    age: int
    satisfaction_environnement: int
    note_evaluation_precedente: float
    niveau_hierarchique: int
    satisfaction_travail: int
    satisfaction_equipe: int
    satisfaction_equilibre_pro_perso: int
    nombre_evaluations: int
    note_evaluation_actuelle: float
    heures_supplementaires: bool
    augmentation_salaire_precedente: float
    nb_participations_pee: int
    nb_formations_suivies: int
    code_sondage: str
    niveau_education: str
    domaine_etude: str
    frequence_deplacement: str
    annees_depuis_derniere_promotion: int
    annees_avec_responsable_actuel: int
    tranche_distance_domicile_travail: str

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }
