import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.auth.security import hash_password, create_access_token

client = TestClient(app)

def create_test_user():
    db = SessionLocal()
    existing_user = db.query(User).filter_by(username="testuser").first()
    if not existing_user:
        user = User(username="testuser", hashed_password=hash_password("testpass"))
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()

def get_auth_headers():
    token = create_access_token({"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module", autouse=True)
def setup_user():
    create_test_user()

def test_predict_success():
    payload = {
        "processed_kg": 32000000,
        "commercialized_liters": 31000000,
        "exported_kg": 1500000,
        "imported_kg": 1000000
    }
    headers = get_auth_headers()
    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200
    assert "predicted_production_liters" in response.json()
    assert isinstance(response.json()["predicted_production_liters"], float)

def test_predict_unauthorized():
    payload = {
        "processed_kg": 32000000,
        "commercialized_liters": 31000000,
        "exported_kg": 1500000,
        "imported_kg": 1000000
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 401
