import httpx
import pandas as pd
from bs4 import BeautifulSoup

from app.logging.logger import setup_logger
from app.core.config import settings
from app.services.helpers import parse_category_table
from app.repositories.fallback import load_processing_csv
from app.models.processing_types import GrapeTypeEnum

logger = setup_logger(__name__)

GRAPE_TYPE_TO_SUBOPT = {
    GrapeTypeEnum.viniferas: "subopt_01",
    GrapeTypeEnum.americanas_hibridas: "subopt_02",
    GrapeTypeEnum.uvas_mesa: "subopt_03",
    GrapeTypeEnum.sem_classificacao: "subopt_04",
}

GRAPE_TYPES = {v: k.value for k, v in GRAPE_TYPE_TO_SUBOPT.items()}


def fetch_processing_data(year: int, grape_type: str) -> list[dict]:
    """Scrapes processing data for the given year and grape type (sub-option)."""
    url = f"{settings.processing_url}&subopcao={grape_type}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
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
            quantity_label="Quantity (kg)",
        )

        for item in data:
            item["GrapeType"] = GRAPE_TYPES.get(grape_type, grape_type)

        logger.info(
            f"{len(data)} processing records extracted for year {year} - type {grape_type}."
        )
        return data

    except Exception:
        logger.warning(
            f"Failed to scrape processing data. Fallback enabled for processing year {year} - type {grape_type}."
        )
        return load_processing_csv(year, GRAPE_TYPES.get(grape_type, grape_type))
