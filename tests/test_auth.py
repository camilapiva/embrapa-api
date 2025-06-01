import pytest
from app.auth.security import create_access_token
from app.auth.dependencies import get_current_user
from app.auth.schemas import UserInDB
from fastapi import HTTPException
from jose import jwt
from app.core.config import settings


def test_verify_token_with_valid_user(monkeypatch):
    """
    Should return a valid user object when the token is valid and user exists.
    """
    # Simulates existing user by returning a UserInDB
    monkeypatch.setattr(
        "app.repositories.user_repository.get_user",
        lambda username: UserInDB(username=username, hashed_password="fake")
    )

    token = create_access_token({"sub": "admin"})
    user = get_current_user(token)
    assert isinstance(user, UserInDB)
    assert user.username == "admin"


def test_verify_token_with_invalid_user(monkeypatch):
    """
    Should raise HTTPException when user does not exist.
    """
    from fastapi import HTTPException

    # Simulate user absence
    monkeypatch.setattr(
        "app.repositories.user_repository.get_user",
        lambda username: None
    )

    token = create_access_token({"sub": "ghost"})
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token)
    assert exc_info.value.status_code == 401
    assert "Invalid token or credentials" in str(exc_info.value.detail)


def test_verify_token_with_invalid_jwt():
    """
    Should raise HTTPException when token is invalid or tampered.
    """
    from fastapi import HTTPException

    invalid_token = "this.is.invalid"
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(invalid_token)

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
        get_current_user(token)

    exc = exc_info.value
    assert exc.status_code == 401
    assert exc.detail == "Invalid token or credentials"
    assert exc.headers == {"WWW-Authenticate": "Bearer"}

