from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/question/Hi")
    assert response.status_code == 200
    json=response.json()
    assert json["code"]==20
    
    