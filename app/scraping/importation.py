import httpx
from bs4 import BeautifulSoup
from app.scraping.helpers import parse_trade_table
from app.utils.fallback import load_importation_csv
from app.core.config import settings
from app.logging.logger import setup_logger
from app.models.importation_types import ImportTypeEnum

logger = setup_logger(__name__)

IMPORT_TYPE_TO_SUBOPT = {
    ImportTypeEnum.vinhos_de_mesa: "subopt_01",
    ImportTypeEnum.espumantes: "subopt_02",
    ImportTypeEnum.uvas_frescas: "subopt_03",
    ImportTypeEnum.uvas_passas: "subopt_04",
    ImportTypeEnum.suco_de_uva: "subopt_05",
}

IMPORT_TYPES = {v: k.value for k, v in IMPORT_TYPE_TO_SUBOPT.items()}

def fetch_importation_data(year: int, import_type: str) -> list[dict]:
    """Scrapes importation data for the given year and import type (sub-option)."""
    url = f"{settings.importation_url}&subopcao={import_type}&ano={year}"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})
        if not table:
            raise ValueError("No table found on the page.")

        data = parse_trade_table(table, year, import_type)
        logger.info(f"{len(data)} importation records extracted for year {year} - type {import_type}")
        return data

    except Exception:
        logger.warning(f"Failed to scrape importation data. Fallback enabled for importation year {year} - type {import_type}")
        return load_importation_csv(year, import_type)
