from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.auth.schemas import UserCreate, UserLogin
from app.auth.security import verify_password, create_access_token
from app.repositories.user_repository import get_user, create_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    """
    This route uses JSON payload to register a new user.
    Different from /login which follows OAuth2 standard using form-data.
    """
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    create_user(user.username, user.password)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
