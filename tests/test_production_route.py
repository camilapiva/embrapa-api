import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_production_route_fallback_failure(monkeypatch, access_token):
    """
    Should return 503 when no production data is returned.
    Forces coverage over `if not data` condition.
    """
    from app.routes import production
    monkeypatch.setattr(production, "fetch_production_data", lambda year: [])

    response = client.get("/production/?year=2022", headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 503
    assert response.json()["detail"] == "Unable to fetch production data from Embrapa or fallback."


def test_production_route_without_token():
    """
    Should return 401 if no authentication token is provided.
    """
    response = client.get("/production/?year=2022")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_production_route_success(authorized_client):
    """
    Should return 200 and data when called with valid year and token.
    """
    response = authorized_client.get("/production/?year=2022")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
