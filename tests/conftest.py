import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.user_repository import create_user, get_user, fake_users_db

TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"

@pytest.fixture(scope="module")
def client():
    """
    Fixture that returns a TestClient of the application.
    """
    return TestClient(app)

@pytest.fixture(scope="module")
def test_user(client):
    """
    Ensures that the test user exists in the system prior to testing.
    """
    if TEST_USERNAME in fake_users_db:
      del fake_users_db[TEST_USERNAME]

    create_user(TEST_USERNAME, TEST_PASSWORD)
    return {"username": TEST_USERNAME, "password": TEST_PASSWORD}

@pytest.fixture(scope="module")
def access_token(client, test_user):
    """
    Logs in with the test user and returns the JWT access token.
    """
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, "Login failed in fixture setup"
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def authorized_client(client, access_token):
    """
    Client authenticated with Bearer Token header.
    """
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
