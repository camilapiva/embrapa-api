import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.models.exportation_types import ExportTypeEnum

client = TestClient(app)


@pytest.fixture
def mock_no_export_data():
    """
    Patches the fetch_exportation_data function to simulate no data available.
    """
    with patch("app.routes.exportation.fetch_exportation_data", return_value=[]):
        yield


def test_exportation_route_invalid_type(access_token):
    """
    Should return 422 when the provided export type is invalid (not part of Enum).
    """
    response = client.get(
        "/exportation/?year=2022&type=invalid_type",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["type"] == "enum"
    assert detail["loc"] == ["query", "type"]
    assert detail["msg"].startswith("Input should be")
    assert "Vinhos de mesa" in detail["msg"]


def test_exportation_route_fallback_failure(mock_no_export_data, access_token):
    """
    Should return 503 when no exportation data is available, even with valid parameters.
    """
    valid_type = ExportTypeEnum.vinhos_de_mesa.value
    response = client.get(
        f"/exportation/?year=2022&type={valid_type}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 503
    assert (
        response.json()["detail"]
        == "Unable to fetch exportation data from Embrapa or fallback."
    )


def test_exportation_route_unmapped_enum_value(access_token, monkeypatch):
    """
    Should return 400 if a valid Enum value is not mapped in EXPORT_TYPE_TO_SUBOPT.
    This forces coverage over `if not subopt_code`.
    """
    from app.routes import exportation

    # Patch the dictionary to simulate valid but unmapped enum
    monkeypatch.setitem(
        exportation.EXPORT_TYPE_TO_SUBOPT, ExportTypeEnum.vinhos_de_mesa, None
    )

    response = client.get(
        f"/exportation/?year=2022&type={ExportTypeEnum.vinhos_de_mesa.value}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid export type."
