import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models.processing_types import GrapeTypeEnum

client = TestClient(app)

@pytest.fixture
def mock_no_processing_data():
    """
    Patches the fetch_processing_data function to simulate no data available.
    """
    with patch("app.routes.processing.fetch_processing_data", return_value=[]):
        yield

def test_processing_route_invalid_type(access_token):
    """
    Should return 422 when the provided grape type is invalid (not part of Enum).
    """
    response = client.get("/processing/?year=2022&type=invalid_type", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "enum"
    assert detail["loc"] == ["query", "type"]
    assert "expected" in detail["ctx"]

def test_processing_route_fallback_failure(mock_no_processing_data, access_token):
    """
    Should return 503 when no processing data is available, even with valid parameters.
    """
    valid_type = GrapeTypeEnum.viniferas.value
    response = client.get(f"/processing/?year=2022&type={valid_type}", headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 503
    assert response.json()["detail"] == "Unable to fetch processing data from Embrapa or fallback."

def test_processing_route_unmapped_enum_value(access_token, monkeypatch):
    """
    Should return 400 if a valid Enum value is not mapped in GRAPE_TYPE_TO_SUBOPT.
    This forces coverage over `if not subopt_code`.
    """
    from app.routes import processing

    monkeypatch.setitem(processing.GRAPE_TYPE_TO_SUBOPT, GrapeTypeEnum.sem_classificacao, None)

    response = client.get(f"/processing/?year=2022&type={GrapeTypeEnum.sem_classificacao.value}", headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid grape type."