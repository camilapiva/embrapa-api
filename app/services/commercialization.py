import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.logging.logger import setup_logger
from app.services.helpers import parse_category_table
from app.repositories.fallback import load_commercialization_csv

logger = setup_logger(__name__)

def fetch_commercialization_data(year: int) -> list[dict]:
    url = f"{settings.commercialization_url}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            raise ValueError("No data table found on the page.")

        data = parse_category_table(
            table=table,
            year=year,
            category_label="Category",
            subcategory_label="Product",
            quantity_label="Quantity (L.)"
        )

        logger.info(f"{len(data)} commercialization records extracted for year {year}")
        return data

    except Exception:
        logger.warning(f"Failed to scrape commercialization data. Fallback enabled for commercialization year {year}")
        return load_commercialization_csv(year)
