from fastapi.testclient import TestClient
from main import app, model_name


def test_read_healthz():
    with TestClient(app) as client:
        response = client.get("/healthz")
        assert response.status_code == 200


def test_embedding_str():
    with TestClient(app) as client:
        embedding_request = {
            "input": "substratus.ai has some great LLM OSS projects for K8s",
            "model": model_name,
        }
        response = client.post("/v1/embeddings", json=embedding_request)
        assert response.status_code == 200
        embedding_response = response.json()
        assert isinstance(embedding_response["data"], list)
        assert isinstance(embedding_response["data"][0]["embedding"], list)
        assert isinstance(embedding_response["data"][0]["embedding"][0], float)


def test_embedding_list_str():
    with TestClient(app) as client:
        embedding_request = {
            "input": [
                "substratus.ai has some great LLM OSS projects for K8s",
                "2nd string",
            ],
            "model": model_name,
        }
        response = client.post("/v1/embeddings", json=embedding_request)
        assert response.status_code == 200
        embedding_response = response.json()
        assert isinstance(embedding_response["data"], list)
        assert isinstance(embedding_response["data"][0]["embedding"], list)
        assert isinstance(embedding_response["data"][0]["embedding"][0], float)

        assert isinstance(embedding_response["data"], list)
        assert isinstance(embedding_response["data"][1]["embedding"], list)
        assert isinstance(embedding_response["data"][1]["embedding"][0], float)

        embedding_1 = embedding_response["data"][0]["embedding"]
        embedding_2 = embedding_response["data"][1]["embedding"]
        assert embedding_1 != embedding_2
