from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TrainInput(BaseModel):
    param_grid: Optional[Dict[str, List[Any]]] = Field(
        default=None,
        description="Grille de paramètres pour l'optimisation (GridSearchCV).",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "param_grid": {
                    "n_estimators": [100, 200],
                    "max_depth": [None, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                    "class_weight": ["balanced", "balanced_subsample"]
                }
            }
        }
    }

class PredictionInput(BaseModel):
    revenu_mensuel: float
    departement: str
    poste: str
    nombre_experiences_precedentes: int
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    age_rh: str
    satisfaction_employee_environnement: int
    note_evaluation_precedente: float
    niveau_hierarchique_poste: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    note_evaluation_actuelle: float
    heure_supplementaires: str
    augementation_salaire_precedente: str
    nombre_participation_pee: int
    nb_formations_suivies: int
    niveau_education: str
    domaine_etude: str
    frequence_deplacement: str
    annees_depuis_la_derniere_promotion: int
    annes_sous_responsable_actuel: int
    tranche_distance_domicile_travail: str

    model_config = {
        "json_schema_extra": {
            "example": {
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
                "tranche_distance_domicile_travail": "10-20km"
            }
        }
    }
