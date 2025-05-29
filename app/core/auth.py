from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.logging.logger import setup_logger

logger = setup_logger(__name__)

def create_access_token(data: dict) -> str:
    """Generate a JWT access token with expiration."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        logger.debug("Access token generated successfully")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to generate access token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed")

def verify_token(token: str) -> dict | None:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        logger.debug("Token verified successfully")
        return payload
    except JWTError:
        logger.warning("Invalid or expired token provided")
        return None

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Dependency to enforce authentication on protected routes."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload