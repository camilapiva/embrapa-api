import httpx
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
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
            print(f"⚠️ Tabela de dados não encontrada para {year}")
            return None

        rows = table.find_all("tr")
        data = []
        current_category = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 2:
                continue

            produto = cols[0].get_text(strip=True)
            quantidade_raw = cols[1].get_text(strip=True)

            # Linha de total
            if produto.lower() == "total":
                try:
                    quantidade = float(quantidade_raw.replace(".", "").replace(",", "."))
                except ValueError:
                    quantidade = None

                data.append({
                    "Categoria": "TOTAL",
                    "Produto": "Total",
                    "Quantidade (L.)": quantidade,
                    "Ano": year
                })
                continue

            # Se for uma categoria principal
            if quantidade_raw == "":
                current_category = produto
                continue

            # Subcategoria ou produto
            try:
                quantidade = float(quantidade_raw.replace(".", "").replace(",", ".")) \
                    if quantidade_raw != "-" else None
            except ValueError:
                quantidade = None

            data.append({
                "Categoria": current_category,
                "Produto": produto,
                "Quantidade (L.)": quantidade,
                "Ano": year
            })

        return pd.DataFrame(data)

    except Exception as e:
        print(f"Erro ao processar {year}: {e}")
        return None

def main():
    os.makedirs("data", exist_ok=True)
    all_data = []

    for year in range(1970, 2024):
        print(f"🔄 Coletando dados de {year}...")
        df = fetch_year_data(year)
        if df is not None:
            all_data.append(df)
        time.sleep(1)  # Evita sobrecarga no servidor

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df.to_csv("data/production.csv", index=False, encoding="utf-8-sig")
        print("Dados salvos em data/production.csv")
    else:
        print("Nenhum dado foi coletado.")

if __name__ == "__main__":
    main()
