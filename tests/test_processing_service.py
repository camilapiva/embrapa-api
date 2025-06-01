import pytest
from app.services import processing
from app.models.processing_types import GrapeTypeEnum

def test_processing_service_table_missing(monkeypatch):
    """
    Should return fallback when no HTML table is found.
    This covers the block where ValueError is raised and caught.
    """
    def mock_httpx_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = "<html><body><p>No table here</p></body></html>"
            def raise_for_status(self): pass
        return MockResponse()

    monkeypatch.setattr(processing.httpx, "get", mock_httpx_get)
    monkeypatch.setattr(
        processing,
        "load_processing_csv",
        lambda year, grape_type: [{"Year": year, "Category": "Fallback", "Product": "Mock", "Quantity (L.)": 999}]
    )

    data = processing.fetch_processing_data(2022, GrapeTypeEnum.viniferas.value)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"


def test_processing_service_fallback(monkeypatch):
    """
    Should return fallback data when scraping raises an unexpected Exception.
    This covers the fallback block explicitly.
    """
    def raise_exception(*args, **kwargs):
        raise RuntimeError("Unexpected scraping error")

    monkeypatch.setattr(processing.httpx, "get", raise_exception)
    monkeypatch.setattr(
        processing,
        "load_processing_csv",
        lambda year, grape_type: [{"Year": year, "Category": "Fallback", "Product": "Mock", "Quantity (L.)": 999}]
    )

    data = processing.fetch_processing_data(2022, GrapeTypeEnum.viniferas.value)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"
