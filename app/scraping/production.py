import httpx
import pandas as pd
import traceback
import numpy as np
from io import StringIO
from bs4 import BeautifulSoup

from app.core.config import settings
from app.logging import logger
from app.utils.fallback import load_production_csv


def fetch_production_data(ano: int) -> list[dict]:
    url = f"{settings.production_url}&ano={ano}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="tb_base tb_dados")

        if not table:
            raise ValueError("Tabela principal não encontrada.")

        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else []

        current_category = None
        data = []

        for row in rows:
            cols = row.find_all("td")
            if not cols or len(cols) < 2:
                continue

            td_classes = [td.get("class", []) for td in cols]

            # Verifica se é categoria (ambos td com classe tb_item)
            if all("tb_item" in cls for cls in td_classes):
                current_category = cols[0].get_text(strip=True)
                continue

            # Verifica se é subitem (ambos td com classe tb_subitem)
            if all("tb_subitem" in cls for cls in td_classes):
                produto = cols[0].get_text(strip=True)
                quantidade = cols[1].get_text(strip=True).replace(".", "").replace(",", ".")

                try:
                    quantidade = float(quantidade) if quantidade != "-" else None
                except ValueError:
                    quantidade = None

                data.append({
                    "Categoria": current_category,
                    "Produto": produto,
                    "Quantidade (L.)": quantidade,
                    "Ano": ano
                })

        # TOTAL
        tfoot = table.find("tfoot", class_="tb_total")
        if tfoot:
            total_row = tfoot.find("tr")
            if total_row:
                tds = total_row.find_all("td")
                if len(tds) == 2:
                    label = tds[0].get_text(strip=True)
                    value = tds[1].get_text(strip=True).replace(".", "").replace(",", ".")

                    try:
                        value = float(value) if value != "-" else None
                    except ValueError:
                        value = None

                    data.append({
                        "Categoria": "Total",
                        "Produto": label,
                        "Quantidade (L.)": value,
                        "Ano": ano
                    })

        logger.info(f"{len(data)} registros extraídos para o ano {ano}.")
        return data

    except Exception:
        logger.warning("Scraping failed. Trying fallback CSV...")
        return load_production_csv(ano)
