import httpx
import pandas as pd
from bs4 import BeautifulSoup
from typing import Literal

from app.logging.logger import setup_logger
from app.core.config import settings
from app.scraping.helpers import parse_category_table
from app.utils.fallback import load_processing_csv

logger = setup_logger(__name__)

# Valid processing types from the Embrapa interface
ProcessingType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

def fetch_processing_data(year: int, grape_type: ProcessingType) -> list[dict]:
    """
    Scrapes processing data for the given year and grape type (sub-option).

    - grape_type:
        subopt_01: Vinifera grapes
        subopt_02: American and hybrid grapes
        subopt_03: Table grapes
        subopt_04: Unclassified grapes
    """
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
            item_label="Cultivar",
            quantity_label="Quantity (kg)"
        )
        
        logger.info(f"{len(data)} processing records extracted for year {year} - type {grape_type}.")
        return data

    except Exception:
        logger.warning(f"Failed to scrape processing data. Fallback enabled for processing year {year} - type {grape_type}.")
        return load_processing_csv(year, grape_type)
