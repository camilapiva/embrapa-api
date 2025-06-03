import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.logging.logger import setup_logger
from app.repositories.fallback import load_production_csv
from app.services.helpers import parse_category_table

logger = setup_logger(__name__)


def fetch_production_data(year: int) -> list[dict]:
    url = f"{settings.production_url}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            raise ValueError("No table with class 'tb_base tb_dados' found.")

        data = parse_category_table(
            table=table,
            year=year,
            category_label="Category",
            subcategory_label="Product",
            quantity_label="Quantity (L.)",
        )

        logger.info(f"{len(data)} production records extracted for year {year}.")
        return data

    except Exception:
        logger.warning(
            f"Failed to scrape production data. Fallback enabled for production year {year}"
        )
        return load_production_csv(year)
