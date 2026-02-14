from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_weather_missing_param():
    response = client.get("/weather")
    assert response.status_code == 422      # FastAPI validation
