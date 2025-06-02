import pytest
from app.services import production


def test_production_service_table_missing(monkeypatch):
    """
    Should return fallback when no HTML table is found.
    This covers the block where ValueError is raised and caught.
    """

    def mock_httpx_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = "<html><body><p>No table here</p></body></html>"

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(production.httpx, "get", mock_httpx_get)
    monkeypatch.setattr(
        production,
        "load_production_csv",
        lambda year: [
            {
                "Year": year,
                "Category": "Fallback",
                "Product": "Mock",
                "Quantity (L.)": 999,
            }
        ],
    )

    data = production.fetch_production_data(2022)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"


def test_production_service_fallback(monkeypatch):
    """
    Should return fallback data when scraping raises an unexpected Exception.
    This covers the fallback block explicitly.
    """

    def raise_exception(*args, **kwargs):
        raise RuntimeError("Unexpected scraping error")

    monkeypatch.setattr(production.httpx, "get", raise_exception)
    monkeypatch.setattr(
        production,
        "load_production_csv",
        lambda year: [
            {
                "Year": year,
                "Category": "Fallback",
                "Product": "Mock",
                "Quantity (L.)": 999,
            }
        ],
    )

    data = production.fetch_production_data(2022)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"
