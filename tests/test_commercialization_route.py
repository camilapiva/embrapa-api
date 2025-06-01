import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

@pytest.fixture
def mocked_no_data():
    """
    Patches the fetch_commercialization_data function to simulate no data available.
    Applied directly to the route's namespace for correct effect.
    """
    with patch("app.routes.commercialization.fetch_commercialization_data", return_value=[]):
        yield

def test_commercialization_route_handles_fallback_failure(mocked_no_data, access_token):
    """
    Should return 503 when commercialization data is unavailable, even with valid year.
    """
    response = client.get("/commercialization/?year=2022", headers={
        "Authorization": f"Bearer {access_token}"
    })

    assert response.status_code == 503
    assert response.json()["detail"] == "Unable to fetch commercialization data or fallback."
