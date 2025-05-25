from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_importation_without_token():
    response = client.get("/importation/?year=2022&import_type=subopt_01")
    assert response.status_code in [401, 403]

def test_importation_with_token():
    login = client.post("/auth/login", data={"username": "admin", "password": "admin"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/importation/", headers=headers, params={"year": 2022, "import_type": "subopt_01"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
