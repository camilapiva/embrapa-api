import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.core.config import settings
from app.scraping.helpers import clean_quantity
from app.logging.logger import setup_logger
from app.models.exportation_types import ExportTypeEnum

logger = setup_logger(__name__)

EXPORT_TYPES = {
    "subopt_01": ExportTypeEnum.vinhos_de_mesa.value,
    "subopt_02": ExportTypeEnum.espumantes.value,
    "subopt_03": ExportTypeEnum.uvas_frescas.value,
    "subopt_04": ExportTypeEnum.uvas_passas.value,
}

def fetch_year_export_data(year: int, export_type: str) -> pd.DataFrame:
    url = f"{settings.exportation_url}&subopcao={export_type}&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            logger.warning(f"Table not found for year {year} - type {export_type}")
            return None

        data = []
        current_type_label = EXPORT_TYPES.get(export_type, export_type)

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) != 3:
                continue

            td1, td2, td3 = cols
            country = td1.get_text(strip=True)
            quantity = clean_quantity(td2.get_text(strip=True))
            value = clean_quantity(td3.get_text(strip=True))

            data.append({
                "Type": current_type_label,
                "Country": country,
                "Quantity (kg)": quantity,
                "Value (US$)": value,
                "Year": year
            })

        total_row = table.select_one("tfoot tr")
        if total_row:
            tds = total_row.find_all("td")
            if len(tds) == 3:
                data.append({
                    "Type": current_type_label,
                    "Country": "Total",
                    "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                    "Value (US$)": clean_quantity(tds[2].get_text(strip=True)),
                    "Year": year
                })

        return pd.DataFrame(data)

    except Exception as e:
        logger.error(f"Error processing exportation for year {year} - type {export_type}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for export_type in EXPORT_TYPES:
            logger.info(f"Collecting exportation data for year {year} - type {export_type}...")
            df = fetch_year_export_data(year, export_type)
            if df is not None:
                all_data.append(df)
            time.sleep(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/exportation.csv", index=False, encoding="utf-8-sig")
        logger.info("File saved to data/exportation.csv")
    else:
        logger.warning("No exportation data was collected.")

if __name__ == "__main__":
    main()
