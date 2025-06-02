from pydantic import BaseModel

class PredictionInput(BaseModel):
    processed_kg: float
    commercialized_liters: float
    exported_kg: float
    imported_kg: float
