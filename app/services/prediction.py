import joblib
import os
import numpy as np

# Absolute path to the model, starting from the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_PATH = os.path.join(BASE_DIR, "notebooks", "model_production_prediction.pkl")


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model not found at: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def make_prediction(data: dict):
    model = load_model()
    features = np.array(
        [
            [
                data["processed_kg"],
                data["commercialized_liters"],
                data["exported_kg"],
                data["imported_kg"],
            ]
        ]
    )
    prediction = model.predict(features)
    return float(prediction[0])
