import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.core.config import settings
from app.scraping.helpers import clean_quantity
from app.logging.logger import setup_logger
from app.models.processing_types import GrapeTypeEnum

logger = setup_logger(__name__)

GRAPE_TYPES = {
    "subopt_01": GrapeTypeEnum.viniferas.value,
    "subopt_02": GrapeTypeEnum.americanas_hibridas.value,
    "subopt_03": GrapeTypeEnum.uvas_mesa.value,
    "subopt_04": GrapeTypeEnum.sem_classificacao.value,
}

def fetch_year_type_data(year: int, grape_type: str) -> pd.DataFrame:
    url = f"{settings.processing_url}&subopcao={grape_type}&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            logger.warning(f"Table not found for year {year} - type {grape_type}")
            return None

        data = []
        current_category = None

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            td1, td2 = cols
            label = td1.get_text(strip=True)
            quantity_raw = td2.get_text(strip=True)
            quantity = clean_quantity(quantity_raw)

            if "tb_item" in td1.get("class", []):
                current_category = label
                if quantity_raw.strip():
                    data.append({
                        "GrapeType": GRAPE_TYPES.get(grape_type, grape_type),
                        "Category": current_category,
                        "Cultivar": "Total",
                        "Quantity (kg)": quantity,
                        "Year": year
                    })
            elif "tb_subitem" in td1.get("class", []):
                data.append({
                    "GrapeType": GRAPE_TYPES.get(grape_type, grape_type),
                    "Category": current_category,
                    "Cultivar": label,
                    "Quantity (kg)": clean_quantity(quantity_raw),
                    "Year": year
                })

        total_row = table.select_one("tfoot tr")
        if total_row:
            tds = total_row.find_all("td")
            if len(tds) == 2:
                data.append({
                    "GrapeType": GRAPE_TYPES.get(grape_type, grape_type),
                    "Category": "Total",
                    "Cultivar": tds[0].get_text(strip=True),
                    "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                    "Year": year
                })

        return pd.DataFrame(data)

    except Exception as e:
        logger.error(f"Error processing for year {year} - type {grape_type}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for grape_type in GRAPE_TYPES:
            logger.info(f"Collecting processing data for year {year} - type {grape_type}...")
            df = fetch_year_type_data(year, grape_type)
            if df is not None:
                all_data.append(df)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/processing.csv", index=False, encoding="utf-8-sig")
        print("File saved to data/processing.csv")
    else:
        print("No processing data was collected.")

if __name__ == "__main__":
    main()
