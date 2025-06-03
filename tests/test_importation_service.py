import pytest
from app.services import importation
from app.models.importation_types import ImportTypeEnum


def test_importation_service_table_missing(monkeypatch):
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

    monkeypatch.setattr(importation.httpx, "get", mock_httpx_get)
    monkeypatch.setattr(
        importation,
        "load_importation_csv",
        lambda year, import_type: [
            {
                "Year": year,
                "Category": "Fallback",
                "Product": "Mock",
                "Quantity (kg)": 999,
            }
        ],
    )

    data = importation.fetch_importation_data(2022, ImportTypeEnum.vinhos_de_mesa.value)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"


def test_importation_service_fallback(monkeypatch):
    """
    Should return fallback data when scraping raises an unexpected Exception.
    This covers the fallback block explicitly.
    """

    def raise_exception(*args, **kwargs):
        raise RuntimeError("Unexpected scraping error")

    monkeypatch.setattr(importation.httpx, "get", raise_exception)
    monkeypatch.setattr(
        importation,
        "load_importation_csv",
        lambda year, import_type: [
            {
                "Year": year,
                "Category": "Fallback",
                "Product": "Mock",
                "Quantity (kg)": 999,
            }
        ],
    )

    data = importation.fetch_importation_data(2022, ImportTypeEnum.vinhos_de_mesa.value)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"
