from fastapi.testclient import TestClient
from app.main import app
from app.models.exportation_types import ExportTypeEnum

client = TestClient(app)

def test_exportation_without_token():
    response = client.get("/exportation/", params={"year": 2022, "type":
    ExportTypeEnum.vinhos_de_mesa.value})
    assert response.status_code in [401, 403]

def test_exportation_with_token():
    login_response = client.post("/auth/login", data={"username": "admin","password": "admin"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/exportation/", headers=headers, params={"year": 2022, "type":
    ExportTypeEnum.vinhos_de_mesa.value
    })

    assert response.status_code == 200
    assert isinstance(response.json(), list)
