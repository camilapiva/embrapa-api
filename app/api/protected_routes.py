from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

router = APIRouter(prefix="/secure", tags=["Protected"])

@router.get("/profile")
def get_profile(user_data: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user_data['sub']}! You are authenticated."}
