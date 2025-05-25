import httpx
import pandas as pd
from bs4 import BeautifulSoup
from typing import Literal

from app.logging.logger import setup_logger
from app.core.config import settings
from app.scraping.helpers import parse_category_table
from app.utils.fallback import load_processing_csv

logger = setup_logger(__name__)

ProcessingType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

GRAPE_TYPES = {
    "subopt_01": "Viníferas",
    "subopt_02": "Americanas e híbridas",
    "subopt_03": "Uvas de mesa",
    "subopt_04": "Sem classificação"
}

def fetch_processing_data(year: int, grape_type: ProcessingType) -> list[dict]:
    """Scrapes processing data for the given year and grape type (sub-option)."""
    url = f"{settings.processing_url}&subopcao={grape_type}&ano={year}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            raise ValueError("No table found on the page.")

        data = parse_category_table(
            table=table,
            year=year,
            category_label="Category",
            subcategory_label="Cultivar",
            quantity_label="Quantity (kg)"
        )

        for item in data:
            item["GrapeType"] = GRAPE_TYPES[grape_type]
        
        logger.info(f"{len(data)} processing records extracted for year {year} - type {grape_type}.")
        return data

    except Exception:
        logger.warning(f"Failed to scrape processing data. Fallback enabled for processing year {year} - type {grape_type}.")
        return load_processing_csv(year, grape_type)
