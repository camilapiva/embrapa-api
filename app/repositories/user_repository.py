from typing import Optional
from app.auth.schemas import UserInDB
from app.auth.security import hash_password

# Fake users
fake_users_db: dict[str, UserInDB] = {
    "admin": UserInDB(username="admin", hashed_password=hash_password("admin"))
}

def get_user(username: str) -> Optional[UserInDB]:
    return fake_users_db.get(username)

def create_user(username: str, password: str) -> UserInDB:
    hashed = hash_password(password)
    user = UserInDB(username=username, hashed_password=hashed)
    fake_users_db[username] = user
    return user
