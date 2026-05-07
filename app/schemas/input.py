from pydantic import BaseModel

class PredictionInput(BaseModel):
    age: int
    salary: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 30,
                "salary": 2500.0
            }
        }
    }
