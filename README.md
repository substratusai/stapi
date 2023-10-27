# Sentence Transformers API

OpenAI compatible embedding endpoint that uses Sentence Transformer for embedding models

## Usage (Docker)
Run the API locally using Docker:
```
docker run -p 8080:8080 -d ghcr.io/substratusai/sentence-transformers-api
```

Now you can visit the API docs on [http://localhost:8080/docs][http://localhost:8080/docs]

You can also use CURL to get embeddings:
```bash
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Your text string goes here",
    "model": "all-MiniLM-L6-v2"
  }'
```

Even the OpenAI Python client can be used to get embeddings:
```python
import openai
openai.api_base = "http://localhost:8080/v1"
openai.api_key = "this isn't used but openai client requires it"
model = "all-MiniLM-L6-v2"
embedding = openai.Embedding.create(input="Some text", model=model)["data"][0]["embedding"]
print(embedding)
```

## Integrations
It's easy to utilize the embedding server with various other tools because
the API is compatible with the OpenAI Embedding API.

### Weaviate
TODO Write weaviate guide here

## Local Development
```
python -m venv .venv
pip install -r requirements.txt
uvicorn main:app --reload
```

Go to http://localhost:8000/docs and try out
