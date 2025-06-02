import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.core.config import settings
from app.services.helpers import clean_quantity
from app.logging.logger import setup_logger
from app.models.importation_types import ImportTypeEnum

logger = setup_logger(__name__)

IMPORT_TYPES = {
    "subopt_01": ImportTypeEnum.vinhos_de_mesa.value,
    "subopt_02": ImportTypeEnum.espumantes.value,
    "subopt_03": ImportTypeEnum.uvas_frescas.value,
    "subopt_04": ImportTypeEnum.uvas_passas.value,
    "subopt_05": ImportTypeEnum.suco_de_uva.value,
}


def fetch_year_import_data(year: int, import_type: str) -> pd.DataFrame:
    url = f"{settings.importation_url}&subopcao={import_type}&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            logger.warning(f"Table not found for year {year} - type {import_type}")
            return None

        data = []
        current_type_label = IMPORT_TYPES.get(import_type, import_type)

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) != 3:
                continue

            td1, td2, td3 = cols
            country = td1.get_text(strip=True)
            quantity = clean_quantity(td2.get_text(strip=True))
            value = clean_quantity(td3.get_text(strip=True))

            data.append(
                {
                    "Type": current_type_label,
                    "Country": country,
                    "Quantity (kg)": quantity,
                    "Value (US$)": value,
                    "Year": year,
                }
            )

        return pd.DataFrame(data)

    except Exception as e:
        logger.error(
            f"Error processing importation for year {year} - type {import_type}: {e}"
        )
        return None


def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for import_type in IMPORT_TYPES:
            logger.info(
                f"Collecting importation data for year {year} - type {import_type}..."
            )
            df = fetch_year_import_data(year, import_type)
            if df is not None:
                all_data.append(df)
            time.sleep(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/importation.csv", index=False, encoding="utf-8-sig")
        logger.info("File saved to data/importation.csv")
    else:
        logger.warning("No importation data was collected.")


if __name__ == "__main__":
    main()
