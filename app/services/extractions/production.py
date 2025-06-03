import httpx
from bs4 import BeautifulSoup
from app.core.config import settings
from app.logging.logger import setup_logger
from app.repositories.fallback import load_production_csv
from app.schemas.schema import ProductionItem, ProductionResponse
from app.services.extractions.base import BaseExtractor
from app.services.extractions.helpers import parse_category_table
from app.services.queryDB.production import fetch_productions_from_db

logger = setup_logger(__name__)

class ProductionExtractor(BaseExtractor):
    
    def fetch_data(year: int) -> list[dict]:
        url = f"{settings.production_url}&ano={year}"
        productions=[]

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = httpx.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "tb_base tb_dados"})

            if not table:
                raise ValueError("No table with class 'tb_base tb_dados' found.")

            data = parse_category_table(
                table=table,
                year=year,
                category_label="Category",
                subcategory_label="Product",
                quantity_label="Quantity (L.)",
            )

            logger.info(f"{len(data)} production records extracted for year {year}.")
            
            for item in data:
                production = ProductionItem(
                    category=item["Category"],
                    product=item["Product"],
                    quantity=item["Quantity (L.)"]
                )
                productions.append(production)

            return ProductionResponse(productions=productions)

        except Exception:
            logger.warning(
                f"Failed to scrape production data. Fallback enabled for production year {year}"
            )
            return fetch_productions_from_db(year)
            # return load_production_csv(year)
