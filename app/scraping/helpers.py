from typing import Optional

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
                "Categoria": "Total",
                "Produto": "Total",
                "Quantidade (L.)": clean_quantity(quantidade_raw),
                "Ano": year
            })
        elif is_category_row(produto, quantidade_raw):
            current_category = produto
        else:
            data.append({
                "Categoria": current_category,
                "Produto": produto,
                "Quantidade (L.)": clean_quantity(quantidade_raw),
                "Ano": year
            })

    return data
