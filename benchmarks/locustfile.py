from locust import HttpUser, task


class EmbeddingUser(HttpUser):
    @task
    def get_embeddings(self):
        embedding_request = {
            "input": "substratus.ai has some great LLM OSS projects for K8s",
            "model": "ignored",
        }
        self.client.post("/v1/embeddings", json=embedding_request)
