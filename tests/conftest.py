import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.user_repository import create_user, get_user_by_username
from app.core.database import SessionLocal

TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"


@pytest.fixture(scope="module")
def client():
    """
    Fixture that returns a TestClient of the application.
    """
    return TestClient(app)


@pytest.fixture(scope="module")
def db():
    """
    Yields a SQLAlchemy DB session for tests.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_user(db):
    """
    Ensures that the test user exists in the system prior to testing.
    """
    existing = get_user_by_username(db, TEST_USERNAME)
    if not existing:
        create_user(db, TEST_USERNAME, TEST_PASSWORD)
    return {"username": TEST_USERNAME, "password": TEST_PASSWORD}


@pytest.fixture(scope="module")
def access_token(client, test_user):
    """
    Logs in with the test user and returns the JWT access token.
    """
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
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
