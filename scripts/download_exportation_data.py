import httpx
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from app.scraping.helpers import clean_quantity

EXPORT_TYPES = {
    "subopt_01": "Vinhos de mesa",
    "subopt_02": "Espumantes",
    "subopt_03": "Uvas frescas",
    "subopt_04": "Suco de uva"
}

def fetch_year_export_data(year: int, export_type: str) -> pd.DataFrame:
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06&subopcao={export_type}&ano={year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})

        if not table:
            print(f"Tabela não encontrada: {year} - {export_type}")
            return None

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

        return pd.DataFrame(data)

    except Exception as e:
        print(f"Erro ao processar {year}-{export_type}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        for export_type in EXPORT_TYPES:
            print(f"Coletando {year} - {export_type}")
            df = fetch_year_export_data(year, export_type)
            if df is not None:
                all_data.append(df)
            time.sleep(1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv("data/exportation.csv", index=False, encoding="utf-8-sig")
        print("Arquivo exportation.csv gerado.")
    else:
        print("Nenhum dado coletado.")

if __name__ == "__main__":
    main()
