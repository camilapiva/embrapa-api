import pytest
from fastapi.testclient import TestClient


@pytest.mark.describe("Production route protection")
class TestProductionAuth:

    def test_without_token(self, client: TestClient):
        response = client.get("/production/?year=2022")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_with_token(self, authorized_client: TestClient):
        response = authorized_client.get("/production/", params={"year": 2022})
        assert response.status_code == 200
        assert isinstance(response.json(), list)
