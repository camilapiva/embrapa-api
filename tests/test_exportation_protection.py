from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_exportation_without_token():
    """Acesso à /exportation sem token deve falhar"""
    response = client.get("/exportation/?year=2022&export_type=subopt_01")
    assert response.status_code in [401, 403]  # depende da política do FastAPI

def test_exportation_with_token():
    """Acesso à /exportation com token válido deve funcionar"""
    login_response = client.post("/auth/login", data={
        "username": "admin",
        "password": "admin"
    })
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/exportation/?year=2022&export_type=subopt_01", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
