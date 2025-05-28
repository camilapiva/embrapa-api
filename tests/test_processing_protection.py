from fastapi.testclient import TestClient
from app.main import app
from app.models.processing_types import GrapeTypeEnum

client = TestClient(app)

def test_importation_without_token():
    response = client.get("/processing/",params={"year": 2022, "type": GrapeTypeEnum.viniferas.value})
    assert response.status_code in [401, 403]

def test_importation_with_token():
    login = client.post("/auth/login", data={"username": "admin", "password": "admin"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/processing/", headers=headers, params={"year": 2022, "type": GrapeTypeEnum.viniferas.value})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
