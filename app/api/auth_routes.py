from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Simulação de usuário (substitua futuramente por validação real)
fake_user = {"username": "admin", "password": "1234"}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    if data.username != fake_user["username"] or data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": data.username})
    return {"access_token": token}
