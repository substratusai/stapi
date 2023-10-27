from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200

def test_embedding_str():
    response = client.get("/healthz")
    assert response.status_code == 200