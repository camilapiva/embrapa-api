import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import TEST_USERNAME, TEST_PASSWORD
from app.repositories.user_repository import create_user, get_user

client = TestClient(app)

@pytest.mark.usefixtures("test_user")
@pytest.mark.parametrize("username,password,status", [
    (TEST_USERNAME, TEST_PASSWORD, 200),
    (TEST_USERNAME, "wrongpass", 401),
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

def test_register_new_user():
    """
    Should register a new user successfully.
    """
    new_user = {"username": "unique_user_123", "password": "newpass"}
    response = client.post("/auth/register", json=new_user)

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_register_existing_user():
    """
    Should raise 400 if username already exists.
    """
    existing_user = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
    create_user(**existing_user)  # Ensure the user exists

    response = client.post("/auth/register", json=existing_user)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"