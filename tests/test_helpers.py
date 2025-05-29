from app.scraping.helpers import clean_quantity, is_total_row, is_category_row, extract_data_rows
from bs4 import BeautifulSoup

def test_clean_quantity_valid():
    assert clean_quantity("123.456,78") == 123456.78
    assert clean_quantity("0") == 0.0

def test_clean_quantity_invalid():
    assert clean_quantity("-") is None
    assert clean_quantity("") is None
    assert clean_quantity(None) is None

def test_is_total_row():
    assert is_total_row("Total") is True
    assert is_total_row(" total ") is True
    assert is_total_row("Subtotal") is False

def test_is_category_row():
    assert is_category_row("VINHO DE MESA", "") is True
    assert is_category_row("SUCO", " ") is True
    assert is_category_row("Tinto", "12345") is False

def test_extract_data_rows():
    html = """
    <table class="tb_base tb_dados">
        <tr><td class="tb_item">VINHO DE MESA</td><td class="tb_item"></td></tr>
        <tr><td class="tb_subitem">Tinto</td><td class="tb_subitem">123.456</td></tr>
        <tr><td class="tb_subitem">Branco</td><td class="tb_subitem">789.000</td></tr>
        <tr><td>Total</td><td>912.456</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")

    result = extract_data_rows(rows, year=2022)

    assert isinstance(result, list)
    assert len(result) == 3

    assert result[0] == {
        "Category": "VINHO DE MESA",
        "Product": "Tinto",
        "Quantity (L.)": 123456.0,
        "Year": 2022
    }
    assert result[2]["Category"] == "Total"
    assert result[2]["Product"] == "Total"
    assert result[2]["Quantity (L.)"] == 912456.0
