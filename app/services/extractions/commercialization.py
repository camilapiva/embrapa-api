from app.schemas.schema import CommercializationItem, CommercializationResponse
from app.services.extractions.base import BaseExtractor
import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.logging.logger import setup_logger
from app.services.extractions.helpers import parse_category_table
from app.repositories.fallback import load_commercialization_csv
from app.services.queryDB.commercialization import fetch_commercializations_from_db

logger = setup_logger(__name__)


class CommercializationExtractor(BaseExtractor):
    

    def fetch_data(year: int) -> list[dict]:
        url = f"{settings.commercialization_url}&ano={year}"
        commercializations = []

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = httpx.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "tb_base tb_dados"})

            if not table:
                raise ValueError("No data table found on the page.")

            data = parse_category_table(
                table=table,
                year=year,
                category_label="Category",
                subcategory_label="Product",
                quantity_label="Quantity (L.)",
            )

            logger.info(f"{len(data)} commercialization records extracted for year {year}")

            for item in data:
                commercialization = CommercializationItem(
                    category=item['category_label'],
                    product=item['subcategory_label'],
                    quantity=item['quantity_label']
                )
                commercializations.append(commercialization)

            return CommercializationResponse(commercializations=commercializations)

        except Exception:
            logger.warning(
                f"Failed to scrape exportation data. Fallback enabled for exportation year {year} - {current_type_label}"
            )

            return fetch_commercializations_from_db(year)