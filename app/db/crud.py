from sqlalchemy.orm import Session
from . import models

def create_input(db: Session, age: int, salary: float):
    db_input = models.InputData(age=age, salary=salary)
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

def create_prediction(db: Session, input_id: int, prediction: int):
    db_prediction = models.PredictionResult(input_id=input_id, prediction=prediction)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def create_interaction_log(db: Session, input_id: int, prediction_id: int, user_input: dict, model_output: dict, status: str):
    db_log = models.InteractionLog(
        input_id=input_id,
        prediction_id=prediction_id,
        user_input=user_input,
        model_output=model_output,
        status=status
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PredictionResult).offset(skip).limit(limit).all()

def get_training_data(db: Session):
    return db.query(models.TrainingDataset).all()
