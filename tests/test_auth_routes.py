import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("username,password,status", [
    ("admin", "admin", 200),
    ("admin", "wrong", 401),
])
def test_login_endpoint(username, password, status):
    response = client.post("/auth/login", data={
        "username": username,
        "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert response.status_code == status
    if status == 200:
        assert "access_token" in response.json()
    else:
        assert response.json()["detail"] == "Invalid credentials"
