import os
import time
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from app.scraping.helpers import clean_quantity
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def fetch_production_data(year: int) -> pd.DataFrame | None:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            logger.warning(f"No table found for year {year}")
            return None

        data = []
        current_category = None

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            label = cols[0].get_text(strip=True)
            quantity_raw = cols[1].get_text(strip=True)

            if label.lower() == "total":
                quantity = clean_quantity(quantity_raw)
                data.append({
                    "Category": "Total",
                    "Product": "Total",
                    "Quantity (L.)": quantity,
                    "Year": year
                })
                continue

            if quantity_raw == "":
                current_category = label
                continue

            quantity = clean_quantity(quantity_raw)
            data.append({
                "Category": current_category,
                "Product": label,
                "Quantity (L.)": quantity,
                "Year": year
            })

        return pd.DataFrame(data)

    except Exception as e:
        logger.error(f"Error processing production for year {year}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        logger.info(f"Collecting production data for year {year}...")
        df = fetch_production_data(year)
        if df is not None:
            all_data.append(df)
        time.sleep(1)

    if all_data:
        result_df = pd.concat(all_data, ignore_index=True)
        result_df.to_csv("data/production.csv", index=False, encoding="utf-8-sig")
        logger.info("Data saved to data/production.csv")
    else:
        logger.warning("No production data was collected.")

if __name__ == "__main__":
    main()