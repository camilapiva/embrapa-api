import pytest
from fastapi.testclient import TestClient
from app.models.exportation_types import ExportTypeEnum

@pytest.mark.describe("Exportation route protection")
class TestExportationAuth:

    def test_without_token(self, client: TestClient):
        response = client.get("/exportation/", params={
            "year": 2022,
            "type": ExportTypeEnum.vinhos_de_mesa.value
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_with_token(self, authorized_client: TestClient):
        response = authorized_client.get("/exportation/", params={
            "year": 2022,
            "type": ExportTypeEnum.vinhos_de_mesa.value
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)
