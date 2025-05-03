from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_invalid_city1():
    response = client.get("/routes/cheapest/?from_city=Москва&to_city=Санкт-Петербург")
    assert response.status_code == 400

def test_invalid_city2():
    response = client.get("/routes/cheapest/?from_city=Луна&to_city=Марс")
    assert response.status_code == 400