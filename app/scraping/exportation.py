import httpx
from bs4 import BeautifulSoup
from typing import Literal

from app.logging import logger
from app.core.config import settings
from app.scraping.helpers import parse_trade_table
from app.utils.fallback import load_exportation_csv

ExportType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

def fetch_exportation_data(year: int, export_type: ExportType) -> list[dict]:
    url = f"{settings.exportation_url}&subopcao={export_type}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})
        if not table:
            raise ValueError("No table found on the page.")

        data = parse_trade_table(table, year, export_type)
        logger.info(f"{len(data)} exportation records extracted for {year} - {export_type}")
        return data

    except Exception:
        logger.warning(f"Fallback used for exportation {year} - {export_type}")
        return load_exportation_csv(year, export_type)
