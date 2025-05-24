import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.core.config import settings
from app.scraping.helpers import clean_quantity

# Tipos de uva disponíveis na interface
GRAPE_TYPES = {
    "subopt_01": "Vinifera",
    "subopt_02": "Americanas e híbridas",
    "subopt_03": "Uvas de mesa",
    "subopt_04": "Sem classificação"
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
            print(f"Tabela não encontrada: {year} - {grape_type}")
            return None

        rows = table.select("tbody tr")
        data = []
        current_category = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            td1, td2 = cols
            label = td1.get_text(strip=True)
            quantity_raw = td2.get_text(strip=True)

            if "tb_item" in td1.get("class", []):
                current_category = label
            elif "tb_subitem" in td1.get("class", []):
                data.append({
                    "GrapeType": grape_type,
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
                    "GrapeType": grape_type,
                    "Category": "Total",
                    "Cultivar": tds[0].get_text(strip=True),
                    "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                    "Year": year
                })

        return pd.DataFrame(data)

    except Exception as e:
        print(f"Erro ao processar {year}-{grape_type}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for grape_type in GRAPE_TYPES:
            print(f"🔄 {year} - {grape_type}")
            df = fetch_year_type_data(year, grape_type)
            if df is not None:
                all_data.append(df)
            time.sleep(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/processing.csv", index=False, encoding="utf-8-sig")
        print("Dados salvos em data/processing.csv")
    else:
        print("Nenhum dado foi coletado.")

if __name__ == "__main__":
    main()
