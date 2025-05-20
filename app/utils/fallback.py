import pandas as pd
import numpy as np
from app.logging import logger

def load_production_csv(ano: int) -> list[dict]:
    try:
        df = pd.read_csv("data/production.csv")
        df = df[df["Ano"] == ano]
        df = df.replace({np.nan: None})
        logger.warning(f"Loaded fallback production data for year {ano}.")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load fallback CSV for {ano}: {e}")
        return []
