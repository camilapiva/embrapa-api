from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
