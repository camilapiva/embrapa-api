import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.services.helpers import clean_quantity
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def fetch_commercialization_data(year: int) -> pd.DataFrame:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04&ano={year}"
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
            label = td1.get_text(strip=True)
            quantity_raw = td2.get_text(strip=True)

            if "tb_item" in td1.get("class", []):
                current_category = label
                if quantity_raw:
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
        logger.error(f"Error processing commercialization for year {year}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        logger.info(f"Collecting commercialization data for year {year}...")
        df = fetch_commercialization_data(year)
        if df is not None:
            all_data.append(df)
        time.sleep(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/commercialization.csv", index=False, encoding="utf-8-sig")
        logger.info("File saved to data/commercialization.csv")
    else:
        logger.warning("No commercialization data was collected.")

if __name__ == "__main__":
    main()