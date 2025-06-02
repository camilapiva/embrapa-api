from fastapi import APIRouter, Depends
from app.schemas.prediction import PredictionInput
from app.services.prediction import make_prediction
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/", dependencies=[Depends(get_current_user)])
def predict(input_data: PredictionInput):
    """
    Predicts the grape production volume based on input features.
    """
    prediction = make_prediction(input_data.model_dump())
    return {"predicted_production_liters": round(prediction, 2)}
