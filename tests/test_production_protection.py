from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_production_without_token():
    response = client.get("/production/?year=2022")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"

def test_production_with_token():
    login_response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/production/", headers=headers, params={"year": 2022})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
