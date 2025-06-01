import pytest
from fastapi.testclient import TestClient

@pytest.mark.describe("Commercialization route protection")
class TestCommercializationAuth:

    def test_without_token(self, client: TestClient):
        response = client.get("/commercialization/?year=2022")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_with_token(self, authorized_client: TestClient):
        response = authorized_client.get("/commercialization/?year=2022")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
