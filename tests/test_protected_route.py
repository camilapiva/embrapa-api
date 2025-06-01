import pytest
from fastapi.testclient import TestClient

@pytest.mark.describe("Protected profile route")
class TestProtectedProfile:

    def test_profile_without_token(self, client: TestClient):
        response = client.get("/secure/profile")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_profile_with_token(self, authorized_client: TestClient):
        response = authorized_client.get("/secure/profile")
        assert response.status_code == 200
        json_data = response.json()
        assert "username" in json_data
        assert "message" in json_data
        assert json_data["username"] == "testuser"
