import pytest
from app.services import commercialization

def test_commercialization_service_table_missing(monkeypatch):
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

    monkeypatch.setattr(commercialization.httpx, "get", mock_httpx_get)
    monkeypatch.setattr(
        commercialization,
        "load_commercialization_csv",
        lambda year: [{"Year": year, "Category": "Fallback", "Product": "Mock", "Quantity (L.)": 999}]
    )

    data = commercialization.fetch_commercialization_data(2022)

    assert isinstance(data, list)
    assert data[0]["Category"] == "Fallback"
