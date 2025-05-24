import pandas as pd
import numpy as np
from app.logging import logger
from typing import Literal

ProcessingType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

def load_production_csv(year: int) -> list[dict]:
    try:
        df = pd.read_csv("data/production.csv")
        df = df[df["Ano"] == year]
        logger.warning(f"Loaded fallback production data for year {year}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load fallback CSV for {year}: {e}")
        return []

def load_processing_csv(year: int, grape_type: ProcessingType) -> list[dict]:
    try:
        df = pd.read_csv("data/processing.csv")
        df = df[(df["Year"] == year) & (df["GrapeType"] == grape_type)]
        logger.warning(f"Loaded fallback processing data for year {year} and type {grape_type}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load fallback CSV for processing {year} ({grape_type}): {e}")
        return []