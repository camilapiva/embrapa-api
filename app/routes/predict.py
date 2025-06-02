from fastapi import APIRouter
from app.schemas.prediction import PredictionInput
from app.services.prediction import make_prediction

router = APIRouter()

@router.post("/predict")
def predict(input_data: PredictionInput):
    prediction = make_prediction(input_data.dict())
    return {"predicted_production_liters": round(prediction, 2)}
