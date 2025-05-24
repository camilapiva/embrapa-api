import httpx
import pandas as pd
import traceback
from bs4 import BeautifulSoup
from typing import Literal

from app.logging import logger
from app.core.config import settings
from app.scraping.helpers import clean_quantity
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

        rows = table.select("tbody tr")
        data = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 3:
                continue

            data.append({
                "Type": export_type,
                "Country": cols[0].get_text(strip=True),
                "Quantity (kg)": clean_quantity(cols[1].get_text(strip=True)),
                "Value (US$)": clean_quantity(cols[2].get_text(strip=True)),
                "Year": year
            })

        total_row = table.select_one("tfoot tr")
        if total_row:
            tds = total_row.find_all("td")
            if len(tds) == 3:
                data.append({
                    "Type": export_type,
                    "Country": "Total",
                    "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                    "Value (US$)": clean_quantity(tds[2].get_text(strip=True)),
                    "Year": year
                })

        logger.info(f"{len(data)} exportation records loaded for {year} - {export_type}")
        return data

    except Exception:
        logger.warning("Failed to scrape exportation data. Trying fallback...")
        return load_exportation_csv(year, export_type)
