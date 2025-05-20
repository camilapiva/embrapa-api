import httpx
import pandas as pd
import traceback
import numpy as np  # ✅ Adicionado aqui
from bs4 import BeautifulSoup
from app.core.config import settings
from app.logging import logger
from io import StringIO

def fetch_production_data() -> list[dict]:
    url = settings.production_url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = httpx.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        if not table:
            raise ValueError("No table found on the page.")

        df = pd.read_html(StringIO(str(table)))[0]
        df.columns = df.columns.map(str).str.strip()

        df = df.dropna(how="all")         # 🧽 Remove linhas completamente vazias
        df = df.dropna(axis=1, how="all") # 🧽 Remove colunas completamente vazias

        logger.info("Production data scraped successfully from Embrapa.")

        # Substituição robusta de NaN por None
        return df.replace({np.nan: None}).to_dict(orient="records")

    except Exception:
        print("Error scraping production data:")
        print(traceback.format_exc())
        logger.error("Error scraping production data:\n" + traceback.format_exc())
        raise
