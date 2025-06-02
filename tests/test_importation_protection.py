import pytest
from fastapi.testclient import TestClient
from app.models.importation_types import ImportTypeEnum


@pytest.mark.describe("Importation route protection")
class TestImportationAuth:

    def test_without_token(self, client: TestClient):
        response = client.get(
            "/importation/",
            params={"year": 2022, "type": ImportTypeEnum.vinhos_de_mesa.value},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_with_token(self, authorized_client: TestClient):
        response = authorized_client.get(
            "/importation/",
            params={"year": 2022, "type": ImportTypeEnum.vinhos_de_mesa.value},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
