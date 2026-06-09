from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
)

# from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class TrainingDataset(Base):
    __tablename__ = "training_dataset"
    id = Column(Integer, primary_key=True, index=True)
    revenu_mensuel = Column(Float)
    departement = Column(String)
    poste = Column(String)
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    age_rh = Column(String)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    niveau_hierarchique_poste = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    heure_supplementaires = Column(String)
    augementation_salaire_precedente = Column(String)
    a_quitte_l_entreprise = Column(Boolean)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    niveau_education = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    tranche_distance_domicile_travail = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InputData(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True, index=True)
    revenu_mensuel = Column(Float)
    departement = Column(String)
    poste = Column(String)
    nombre_experiences_precedentes = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)
    age_rh = Column(String)
    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    niveau_hierarchique_poste = Column(Integer)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    heure_supplementaires = Column(String)
    augementation_salaire_precedente = Column(String)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    niveau_education = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_la_derniere_promotion = Column(Integer)
    annes_sous_responsable_actuel = Column(Integer)
    tranche_distance_domicile_travail = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    predictions = relationship("PredictionResult", back_populates="input")
    interaction_logs = relationship("InteractionLog", back_populates="input")


class PredictionResult(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    prediction = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    input = relationship("InputData", back_populates="predictions")
    interaction_logs = relationship(
        "InteractionLog", back_populates="prediction_result"
    )


class InteractionLog(Base):
    __tablename__ = "interaction_logs"
    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    user_input = Column(JSON)
    model_output = Column(JSON)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    input = relationship("InputData", back_populates="interaction_logs")
    prediction_result = relationship(
        "PredictionResult", back_populates="interaction_logs"
    )
