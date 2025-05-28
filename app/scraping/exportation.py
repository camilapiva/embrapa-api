import httpx
from bs4 import BeautifulSoup
from app.logging.logger import setup_logger
from app.core.config import settings
from app.scraping.helpers import parse_trade_table
from app.utils.fallback import load_exportation_csv
from app.models.exportation_types import ExportTypeEnum

logger = setup_logger(__name__)

EXPORT_TYPE_TO_SUBOPT = {
    ExportTypeEnum.vinhos_de_mesa: "subopt_01",
    ExportTypeEnum.espumantes: "subopt_02",
    ExportTypeEnum.uvas_frescas: "subopt_03",
    ExportTypeEnum.uvas_passas: "subopt_04",
}

EXPORT_TYPES = {v: k.value for k, v in EXPORT_TYPE_TO_SUBOPT.items()}

def fetch_exportation_data(year: int, export_type: str) -> list[dict]:
    """Scrapes exportation data for the given year and import type (sub-option)."""
    url = f"{settings.exportation_url}&subopcao={export_type}&ano={year}"
    current_type_label = EXPORT_TYPES.get(export_type, export_type)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "tb_base tb_dados"})
        if not table:
            raise ValueError("No table found on the page.")

        data = parse_trade_table(table, year, current_type_label)
        logger.info(f"{len(data)} exportation records extracted for year {year} - {current_type_label}")
        return data

    except Exception:
        logger.warning(f"Failed to scrape exportation data. Fallback enabled for exportation year {year} - {current_type_label}")
        return load_exportation_csv(year, current_type_label)
