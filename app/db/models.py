from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class TrainingDataset(Base):
    __tablename__ = "training_dataset"
    id = Column(Integer, primary_key=True, index=True)
    revenu_mensuel = Column(Float)
    departement = Column(String)
    poste = Column(String)
    nb_experiences_precedentes = Column(Integer)
    annees_experience_totale = Column(Integer)
    annees_dans_entreprise = Column(Integer)
    annees_poste_actuel = Column(Integer)
    age = Column(Integer)
    satisfaction_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    niveau_hierarchique = Column(Integer)
    satisfaction_travail = Column(Integer)
    satisfaction_equipe = Column(Integer)
    satisfaction_equilibre_pro_perso = Column(Integer)
    nombre_evaluations = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    heures_supplementaires = Column(Boolean)
    augmentation_salaire_precedente = Column(Float)
    a_quitte_entreprise = Column(Boolean)
    nb_participations_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    code_sondage = Column(String)
    niveau_education = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_derniere_promotion = Column(Integer)
    annees_avec_responsable_actuel = Column(Integer)
    tranche_distance_domicile_travail = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InputData(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True, index=True)
    revenu_mensuel = Column(Float)
    departement = Column(String)
    poste = Column(String)
    nb_experiences_precedentes = Column(Integer)
    annees_experience_totale = Column(Integer)
    annees_dans_entreprise = Column(Integer)
    annees_poste_actuel = Column(Integer)
    age = Column(Integer)
    satisfaction_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    niveau_hierarchique = Column(Integer)
    satisfaction_travail = Column(Integer)
    satisfaction_equipe = Column(Integer)
    satisfaction_equilibre_pro_perso = Column(Integer)
    nombre_evaluations = Column(Integer)
    note_evaluation_actuelle = Column(Float)
    heures_supplementaires = Column(Boolean)
    augmentation_salaire_precedente = Column(Float)
    nb_participations_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    code_sondage = Column(String)
    niveau_education = Column(String)
    domaine_etude = Column(String)
    frequence_deplacement = Column(String)
    annees_depuis_derniere_promotion = Column(Integer)
    annees_avec_responsable_actuel = Column(Integer)
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
    interaction_logs = relationship("InteractionLog", back_populates="prediction_result")

class InteractionLog(Base):
    __tablename__ = "interaction_logs"
    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    user_input = Column(JSONB)
    model_output = Column(JSONB)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    input = relationship("InputData", back_populates="interaction_logs")
    prediction_result = relationship("PredictionResult", back_populates="interaction_logs")
