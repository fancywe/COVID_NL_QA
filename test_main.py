from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_type1():
    
    response = client.get("/question/What's the latest on Covid in the US?")
    assert response.status_code == 200
    json=response.json()
    assert json["code"]==0

def test_read_type2():
    
    response = client.get("/question/Tell me about Covid situation in California?")
    assert response.status_code == 200
    json=response.json()
    assert json["code"]==1
    
def test_read_type3():
    
    response = client.get("/question/How many new Covid cases in Florida?")
    assert response.status_code == 200
    json=response.json()
    assert json["code"]==2
    
    
    