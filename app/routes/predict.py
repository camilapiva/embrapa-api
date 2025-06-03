from fastapi import APIRouter, Depends
from app.schemas.prediction import PredictionInput
from app.services.prediction import make_prediction
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    summary="Predict grape production volume",
    description=(
        "Predicts the annual grape production volume (in liters) based on the following parameters:\n\n"
        "- **processed_kg**: Quantity of grapes processed (in kilograms)\n"
        "- **commercialized_liters**: Volume of grape products commercialized (in liters)\n"
        "- **exported_kg**: Quantity exported (in kilograms)\n"
        "- **imported_kg**: Quantity imported (in kilograms)\n\n"
        "**Example request payload:**\n"
        "```json\n"
        "{\n"
        "  \"processed_kg\": 32000000,\n"
        "  \"commercialized_liters\": 31000000,\n"
        "  \"exported_kg\": 1500000,\n"
        "  \"imported_kg\": 1000000\n"
        "}\n"
        "```"
    ),
    response_description="Estimated grape production volume in liters.",
)
def predict(input_data: PredictionInput):
    """
    Predicts grape production based on historical input features.
    """
    prediction = make_prediction(input_data.model_dump())
    return {"predicted_production_liters": round(prediction, 2)}
