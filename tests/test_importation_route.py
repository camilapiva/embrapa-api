import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models.importation_types import ImportTypeEnum

client = TestClient(app)


@pytest.fixture
def mock_no_import_data():
    """
    Patches the fetch_importation_data function to simulate no data available.
    """
    with patch("app.routes.importation.fetch_importation_data", return_value=[]):
        yield


def test_importation_route_invalid_enum(access_token):
    """
    Should return 422 when the provided import type is not part of Enum.
    """
    response = client.get(
        "/importation/?year=2022&type=invalid_type",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "enum"
    assert detail["loc"] == ["query", "type"]
    assert "expected" in detail["ctx"]


def test_importation_route_fallback_failure(mock_no_import_data, access_token):
    """
    Should return 503 when no importation data is available.
    """
    response = client.get(
        f"/importation/?year=2022&type={ImportTypeEnum.espumantes.value}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 503
    assert (
        response.json()["detail"]
        == "Unable to fetch importation data from Embrapa or fallback."
    )


def test_importation_route_unmapped_enum_value(access_token, monkeypatch):
    """
    Should return 400 if a valid Enum value is not mapped in IMPORT_TYPE_TO_SUBOPT.
    This forces coverage over `if not subopt_code`.
    """
    from app.routes import importation

    monkeypatch.setitem(
        importation.IMPORT_TYPE_TO_SUBOPT, ImportTypeEnum.uvas_passas, None
    )

    response = client.get(
        f"/importation/?year=2022&type={ImportTypeEnum.uvas_passas.value}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid import type."
