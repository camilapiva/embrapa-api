from typing import Optional
from bs4 import Tag

def clean_quantity(value: str) -> Optional[float]:
    """Converte um valor de quantidade para float, tratando '-' e valores vazios."""
    if not value or value.strip() == "-":
        return None
    try:
        return float(value.replace(".", "").replace(",", "."))
    except ValueError:
        return None

def is_total_row(produto: str) -> bool:
    return produto.strip().lower() == "total"

def is_category_row(produto: str, quantidade: str) -> bool:
    return quantidade.strip() == ""

def extract_data_rows(rows, year: int) -> list[dict]:
    """Extrai e organiza os dados da tabela HTML."""
    data = []
    current_category = None

    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 2:
            continue

        produto = cols[0].get_text(strip=True)
        quantidade_raw = cols[1].get_text(strip=True)

        if is_total_row(produto):
            data.append({
                "Category": "Total",
                "Product": "Total",
                "Quantity (L.)": clean_quantity(quantidade_raw),
                "Year": year
            })
        elif is_category_row(produto, quantidade_raw):
            current_category = produto
        else:
            data.append({
                "Category": current_category,
                "Product": produto,
                "Quantity (L.)": clean_quantity(quantidade_raw),
                "Year": year
            })

    return data

def parse_category_table(table: Tag, year: int, category_label: str, subcategory_label: str, quantity_label: str) -> list[dict]:
    data = []
    current_category = None

    for row in table.select("tbody tr"):
        tds = row.find_all("td")
        if len(tds) != 2:
            continue
        td1, td2 = tds

        if "tb_item" in td1.get("class", []):
            current_category = td1.get_text(strip=True)
        elif "tb_subitem" in td1.get("class", []):
            data.append({
                category_label: current_category,
                subcategory_label: td1.get_text(strip=True),
                quantity_label: clean_quantity(td2.get_text(strip=True)),
                "Year": year
            })

    total_row = table.select_one("tfoot tr")
    if total_row:
        tds = total_row.find_all("td")
        if len(tds) == 2:
            data.append({
                category_label: "Total",
                subcategory_label: tds[0].get_text(strip=True),
                quantity_label: clean_quantity(tds[1].get_text(strip=True)),
                "Year": year
            })

    return data


def parse_trade_table(table: Tag, year: int, trade_type: str) -> list[dict]:
    """Extrai dados de tabelas das abas Exportação e Importação."""
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

    total_row = table.select_one("tfoot tr")
    if total_row:
        tds = total_row.find_all("td")
        if len(tds) == 3:
            data.append({
                "Type": trade_type,
                "Country": "Total",
                "Quantity (kg)": clean_quantity(tds[1].get_text(strip=True)),
                "Value (US$)": clean_quantity(tds[2].get_text(strip=True)),
                "Year": year
            })

    return data