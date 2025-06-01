import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.auth.dependencies import get_current_user
from app.auth.schemas import UserInDB
from app.core.config import settings
from app.auth.dependencies import get_current_user as real_get_current_user
from app.repositories import user_repository


class FakeDBSession:
    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def first(self):
        return self.result

    def set_result(self, result):
        self.result = result
        return self


@pytest.fixture
def fake_db():
    return FakeDBSession()


def test_verify_token_with_valid_user(monkeypatch, fake_db):
    """
    Should return a valid user object when the token is valid and user exists.
    """
    def mock_get_user_by_username(db, username):
        return UserInDB(username=username, hashed_password="fake")

    fake_db.set_result(UserInDB(username="admin", hashed_password="fake"))
    monkeypatch.setattr(user_repository, "get_user_by_username", mock_get_user_by_username)

    token = create_access_token({"sub": "admin"})
    user = real_get_current_user(token=token, db=fake_db)
    assert isinstance(user, UserInDB)
    assert user.username == "admin"


def test_verify_token_with_invalid_user(monkeypatch, fake_db):
    """
    Should raise HTTPException when user does not exist.
    """
    def mock_get_user_by_username(db, username):
        return None

    fake_db.set_result(None)
    monkeypatch.setattr(user_repository, "get_user_by_username", mock_get_user_by_username)

    token = create_access_token({"sub": "ghost"})
    with pytest.raises(HTTPException) as exc_info:
        real_get_current_user(token=token, db=fake_db)

    assert exc_info.value.status_code == 401
    assert "Invalid token or credentials" in str(exc_info.value.detail)


def test_verify_token_with_invalid_jwt():
    """
    Should raise HTTPException when token is invalid or tampered.
    """
    invalid_token = "this.is.invalid"
    with pytest.raises(HTTPException) as exc_info:
        real_get_current_user(token=invalid_token, db=None)

    exc = exc_info.value
    assert exc.status_code == 401
    assert "Invalid token or credentials" in str(exc.detail)
    assert exc.headers == {"WWW-Authenticate": "Bearer"}


def test_token_without_sub_claim():
    """
    Should raise HTTPException when the token is valid but missing 'sub' field.
    """
    token = jwt.encode({"some": "data"}, settings.secret_key, algorithm="HS256")

    with pytest.raises(HTTPException) as exc_info:
        real_get_current_user(token=token, db=None)

    exc = exc_info.value
    assert exc.status_code == 401
    assert exc.detail == "Invalid token or credentials"
    assert exc.headers == {"WWW-Authenticate": "Bearer"}
