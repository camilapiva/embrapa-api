import httpx
from bs4 import BeautifulSoup
from app.scraping.helpers import parse_trade_table
from app.utils.fallback import load_importation_csv
from app.core.config import settings
from app.logging import logger

def fetch_importation_data(year: int, import_type: str) -> list[dict]:
    url = f"{settings.importation_url}&subopcao={import_type}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})
        if not table:
            raise ValueError("No table found on the page.")

        data = parse_trade_table(table, year)
        logger.info(f"{len(data)} importation records extracted for {year} - {import_type}")
        return data

    except Exception:
        logger.warning(f"Fallback used for importation {year} - {import_type}")
        return load_importation_csv(year, import_type)
