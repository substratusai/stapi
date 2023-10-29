import random


from locust import HttpUser, task


def random_sentence() -> str:
    subjects = ["I", "You", "Bob", "Sue", "We", "Sam", "Nick", "Bob"]
    verbs = ["eat", "make", "read", "write", "create", "code"]
    objects = [
        "a book",
        "the homework",
        "a poem",
        "a song",
        "an email",
        "some software",
    ]

    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."


class EmbeddingUser(HttpUser):
    @task
    def get_embeddings(self):
        sentence = random_sentence()
        embedding_request = {
            "input": sentence,
            "model": "ignored",
        }
        self.client.post("/v1/embeddings", json=embedding_request)
