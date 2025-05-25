import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.scraping.helpers import clean_quantity
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

IMPORT_TYPES = {
    "subopt_01": "Vinhos de mesa",
    "subopt_02": "Espumantes",
    "subopt_03": "Uvas frescas",
    "subopt_04": "Uvas passas",
    "subopt_05": "Suco de uva"
}

def fetch_year_import_data(year: int, import_type: str) -> pd.DataFrame:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05&subopcao={import_type}&ano={year}"
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
        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) != 3:
                continue

            data.append({
                "Type": import_type,
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
                    "Type": import_type,
                    "Country": "Total",
                    "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                    "Value (US$)": clean_quantity(tds[2].get_text(strip=True)),
                    "Year": year
                })

        return pd.DataFrame(data)

    except Exception as e:
        logger.error(f"Error processing importation for year {year} - type {import_type}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for import_type in IMPORT_TYPES:
            logger.info(f"Collecting importation data for year {year} - type {import_type}...")
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
