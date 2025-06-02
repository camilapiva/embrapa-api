import pytest
from bs4 import BeautifulSoup
from app.services import helpers


def test_clean_quantity_valid():
    assert helpers.clean_quantity("1.234,56") == 1234.56
    assert helpers.clean_quantity("123") == 123.0


def test_clean_quantity_invalid_format():
    assert helpers.clean_quantity("abc") is None
    assert helpers.clean_quantity("") is None
    assert helpers.clean_quantity(None) is None


def test_clean_quantity_triggers_value_error(monkeypatch):
    # Força erro no float
    monkeypatch.setattr(
        "builtins.float", lambda x: (_ for _ in ()).throw(ValueError("mock"))
    )
    result = helpers.clean_quantity("100")
    assert result is None


def test_is_total_row():
    assert helpers.is_total_row("total")
    assert helpers.is_total_row("  TOTAL  ")
    assert not helpers.is_total_row("vinho")


def test_is_category_row():
    assert helpers.is_category_row("vinho", "")
    assert not helpers.is_category_row("vinho", "123")


def test_extract_data_rows():
    html = """
    <table>
        <tr><td>Vinhos</td><td></td></tr>
        <tr><td>Tinto</td><td>1.000</td></tr>
        <tr><td>Total</td><td>1.000</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    result = helpers.extract_data_rows(rows, 2022)

    assert len(result) == 2
    assert result[0]["Category"] == "Vinhos"
    assert result[1]["Product"] == "Total"


def test_extract_data_rows_skips_invalid():
    html = """
    <table>
        <tr><td>Only one</td></tr>
        <tr><td>Too</td><td>many</td><td>columns</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    result = helpers.extract_data_rows(rows, 2022)

    assert result == []  # Ambas devem ser ignoradas


def test_parse_category_table():
    html = """
    <table>
        <tbody>
            <tr><td class="tb_item">Category A</td><td>2.000</td></tr>
            <tr><td class="tb_subitem">SubA1</td><td>1.000</td></tr>
            <tr><td class="tb_subitem">SubA2</td><td>1.000</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    result = helpers.parse_category_table(
        table, 2022, "Categoria", "Produto", "Quantidade"
    )

    assert len(result) == 3
    assert result[0]["Produto"] == "Total"
    assert result[1]["Produto"] == "SubA1"


def test_parse_category_table_skips_invalid():
    html = """
    <table>
        <tbody>
            <tr><td>Only one</td></tr>
            <tr><td>Too</td><td>Many</td><td>Cols</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    result = helpers.parse_category_table(
        table, 2022, "Categoria", "Produto", "Quantidade"
    )

    assert result == []


def test_parse_trade_table():
    html = """
    <table>
        <tbody>
            <tr><td>Brasil</td><td>1.000</td><td>10.000</td></tr>
            <tr><td>Argentina</td><td>2.000</td><td>20.000</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    result = helpers.parse_trade_table(table, 2022, "Vinhos")

    assert len(result) == 2
    assert result[0]["Country"] == "Brasil"
    assert result[1]["Value (US$)"] == 20000.0


def test_parse_trade_table_skips_invalid():
    html = """
    <table>
        <tbody>
            <tr><td>Only one</td></tr>
            <tr><td>Too</td><td>Many</td><td>Cols</td><td>Extra</td></tr>
        </tbody>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    result = helpers.parse_trade_table(table, 2022, "Vinhos")

    assert result == []
