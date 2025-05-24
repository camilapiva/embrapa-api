import httpx
import pandas as pd
import traceback
from bs4 import BeautifulSoup

from app.core.config import settings
from app.logging import logger
from app.utils.fallback import load_production_csv
from app.scraping.helpers import extract_data_rows


def fetch_production_data(ano: int) -> list[dict]:
    url = f"{settings.production_url}&ano={ano}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            raise ValueError("No table with class 'tb_base tb_dados' found.")

        rows = table.find_all("tr")
        data = extract_data_rows(rows, ano)

        if not data:
            raise ValueError("Parsed table is empty.")

        logger.info(f"{len(data)} registros extraídos para o ano {ano}.")
        return data

    except Exception:
        logger.warning("Scraping failed. Trying fallback CSV...")
        return load_production_csv(ano)
