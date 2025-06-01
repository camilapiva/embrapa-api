from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.auth.schemas import UserInDB

router = APIRouter(prefix="/secure", tags=["Protected"])

@router.get("/profile", summary="Get current user profile")
def get_profile(user: UserInDB = Depends(get_current_user)):
    return {
        "username": user.username,
        "message": f"Hello, {user.username}. You are authenticated."
    }
