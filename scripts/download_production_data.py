import httpx
import pandas as pd
from bs4 import BeautifulSoup
import time
import os

def fetch_year_data(year: int) -> pd.DataFrame:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={year}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            print(f"Table not found for year {year}")
            return None

        rows = table.find_all("tr")
        data = []
        current_category = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            label = cols[0].get_text(strip=True)
            quantity_raw = cols[1].get_text(strip=True)

            # Linha de total
            if label.lower() == "total":
                try:
                    quantity  = float(quantity_raw.replace(".", "").replace(",", "."))
                except ValueError:
                    quantity  = None

                data.append({
                    "Category": "Total",
                    "Product": "Total",
                    "Quantity (L.)": quantity,
                    "Year": year
                })
                continue

            # Se for uma categoria principal
            if quantity_raw == "":
                current_category = label
                continue

            # Subcategoria ou produto
            try:
                quantity = float(quantity_raw.replace(".", "").replace(",", ".")) \
                    if quantity_raw != "-" else None
            except ValueError:
                quantity = None

            data.append({
                "Category": current_category,
                "Product": label,
                "Quantity (L.)": quantity,
                "Year": year
            })

        return pd.DataFrame(data)

    except Exception as e:
        print(f"Error processing year {year}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        print(f"Collecting data for {year}...")
        df = fetch_year_data(year)
        if df is not None:
            all_data.append(df)
        time.sleep(1)  # avoid overloading the server

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df.to_csv("data/production.csv", index=False, encoding="utf-8-sig")
        print("File saved to data/production.csv")
    else:
        print("No data was collected.")

if __name__ == "__main__":
    main()
