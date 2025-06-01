import pytest
from fastapi.testclient import TestClient
from app.models.processing_types import GrapeTypeEnum

@pytest.mark.describe("Processing route protection")
class TestProcessingAuth:

    def test_without_token(self, client: TestClient):
        response = client.get(
            "/processing/",
            params={"year": 2022, "type": GrapeTypeEnum.viniferas.value}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_with_token(self, authorized_client: TestClient):
        response = authorized_client.get(
            "/processing/",
            params={"year": 2022, "type": GrapeTypeEnum.viniferas.value}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
