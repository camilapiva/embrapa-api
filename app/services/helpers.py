import re
from typing import Optional
from bs4 import Tag
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def clean_quantity(value: str) -> Optional[float]:
    """Converts quantity string to float. Returns None for any invalid or non-numeric value."""
    if not value:
        return None
    
    cleaned = value.strip().replace(".", "").replace(",", ".")

    if not re.match(r'^-?\d+(\.\d+)?$', cleaned):
        return None

    try:
        return float(cleaned)
    except ValueError:
        logger.warning(f"Invalid quantity format: {value}")
        return None

def is_total_row(produto: str) -> bool:
    return produto.strip().lower() == "total"

def is_category_row(produto: str, quantidade: str) -> bool:
    return quantidade.strip() == ""

def extract_data_rows(rows, year: int) -> list[dict]:
    """Parses raw rows from an HTML table (2-column format)."""
    data = []
    current_category = None

    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 2:
            continue

        label = cols[0].get_text(strip=True)
        quantity_raw = cols[1].get_text(strip=True)

        if is_total_row(label):
            data.append({
                "Category": "Total",
                "Product": "Total",
                "Quantity (L.)": clean_quantity(quantity_raw),
                "Year": year
            })
        elif is_category_row(label, quantity_raw):
            current_category = label
        else:
            data.append({
                "Category": current_category,
                "Product": label,
                "Quantity (L.)": clean_quantity(quantity_raw),
                "Year": year
            })

    logger.debug(f"{len(data)} rows extracted from 2-column table for year {year}")
    return data

def parse_category_table(table: Tag, year: int, category_label: str, subcategory_label: str, quantity_label: str) -> list[dict]:
    data = []
    current_category = None

    for row in table.select("tbody tr"):
        tds = row.find_all("td")
        if len(tds) != 2:
            continue
        td1, td2 = tds

        label = td1.get_text(strip=True)
        quantity_raw = td2.get_text(strip=True)
        quantity = clean_quantity(quantity_raw)

        if "tb_item" in td1.get("class", []):
            current_category = label
            if quantity_raw.strip():
                data.append({
                    category_label: current_category,
                    subcategory_label: "Total",
                    quantity_label: quantity,
                    "Year": year
                })
        elif "tb_subitem" in td1.get("class", []):
            data.append({
                category_label: current_category,
                subcategory_label: td1.get_text(strip=True),
                quantity_label: clean_quantity(td2.get_text(strip=True)),
                "Year": year
            })

    logger.debug(f"{len(data)} rows extracted from category table for year {year}")
    return data


def parse_trade_table(table: Tag, year: int, trade_type: str) -> list[dict]:
    """Parses trade tables (Exportation and Importation style with 3 columns)."""
    data = []

    for row in table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) != 3:
            continue
        data.append({
            "Type": trade_type,
            "Country": cols[0].get_text(strip=True),
            "Quantity (kg)": clean_quantity(cols[1].get_text(strip=True)),
            "Value (US$)": clean_quantity(cols[2].get_text(strip=True)),
            "Year": year
        })

    logger.debug(f"{len(data)} rows extracted from trade table for year {year} - {trade_type}")
    return data