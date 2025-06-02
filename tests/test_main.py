from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": f"Welcome to {app.title}"}


def test_app_lifespan_and_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Welcome to" in response.json()["message"]
