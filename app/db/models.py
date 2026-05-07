from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from .database import Base

class TrainingDataset(Base):
    __tablename__ = "training_dataset"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    salary = Column(Float)
    target = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InputData(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    salary = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PredictionResult(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    prediction = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class InteractionLog(Base):
    __tablename__ = "interaction_logs"
    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("inputs.id"))
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    user_input = Column(JSON) # JSONB en PostgreSQL
    model_output = Column(JSON) # JSONB en PostgreSQL
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
