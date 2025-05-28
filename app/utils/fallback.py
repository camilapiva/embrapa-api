import pandas as pd
import numpy as np
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def load_production_csv(year: int) -> list[dict]:
    try:
        df = pd.read_csv("data/production.csv")
        df = df[df["Year"] == year]
        logger.warning(f"Loaded fallback production data for year {year}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load production fallback CSV for year {year}: {e}")
        return []

def load_processing_csv(year: int, grape_type: str) -> list[dict]:
    try:
        df = pd.read_csv("data/processing.csv")
        df = df[(df["Year"] == year) & (df["GrapeType"] == grape_type)]
        logger.warning(f"Loaded fallback processing data for year {year} and type {grape_type}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load processing fallback CSV for year {year} and type ({grape_type}): {e}")
        return []
    
def load_exportation_csv(year: int, export_type: str) -> list[dict]:
    try:
        df = pd.read_csv("data/exportation.csv")
        df = df[(df["Year"] == year) & (df["Type"] == export_type)]
        logger.warning(f"Loaded fallback exportation data for year {year} and type {export_type}.")
        return df.replace({pd.NA: None, pd.NaT: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load exportation fallback CSV for year {year} and type {export_type}: {e}")
        return []
    
def load_importation_csv(year: int, import_type: str) -> list[dict]:
    try:
        df = pd.read_csv("data/importation.csv")
        df = df[(df["Year"] == year) & (df["Type"] == import_type)]
        logger.warning(f"Loaded fallback importation data for year {year} and type {import_type}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load importation fallback CSV for year {year} and type {import_type}: {e}")
        return []

def load_commercialization_csv(year: int) -> list[dict]:
    try:
        df = pd.read_csv("data/commercialization.csv")
        df = df[df["Year"] == year]
        logger.warning(f"Loaded fallback commercialization data for year {year}.")
        return df.replace({np.nan: None}).to_dict(orient="records")
    except Exception as e:
        logger.error(f"Failed to load commercialization fallback CSV for year {year}: {e}")
        return []
