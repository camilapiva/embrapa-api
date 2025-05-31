import os
import time
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from app.scraping.helpers import clean_quantity
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def fetch_production_data(year: int) -> pd.DataFrame:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            logger.warning(f"Table not found for year {year}")
            return None

        data = []
        current_category = None

        for row in table.select("tbody tr"):
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            td1, td2 = cols
            label = cols[0].get_text(strip=True)
            quantity_raw = td2.get_text(strip=True)

            if "tb_item" in td1.get("class", []):
                current_category = label
                data.append({
                    "Category": current_category,
                    "Product": "Total",
                    "Quantity (L.)": clean_quantity(quantity_raw),
                    "Year": year
                })
            elif "tb_subitem" in td1.get("class", []):
                data.append({
                    "Category": current_category,
                    "Product": label,
                    "Quantity (L.)": clean_quantity(quantity_raw),
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