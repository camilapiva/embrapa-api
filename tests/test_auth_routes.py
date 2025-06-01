import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from tests.conftest import TEST_USERNAME, TEST_PASSWORD
from app.repositories.user_repository import get_user_by_username, create_user
from app.core.database import get_db

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
    db: Session = next(get_db())

    # Garantir que o usuário não exista antes do teste
    existing = get_user_by_username(db, new_user["username"])
    if existing:
        db.delete(existing)
        db.commit()

    response = client.post("/auth/register", json=new_user)

    assert response.status_code == 200
    assert response.json()["username"] == new_user["username"]

    created = get_user_by_username(db, new_user["username"])
    assert created is not None
    assert created.username == new_user["username"]


def test_register_existing_user():
    """
    Should raise 400 if username already exists.
    """
    existing_user = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
    db: Session = next(get_db())

    if not get_user_by_username(db, existing_user["username"]):
        create_user(db, **existing_user)

    response = client.post("/auth/register", json=existing_user)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
