# Sentence Transformers API

OpenAI compatible embedding API that uses Sentence Transformer for embedding models

Support the project by adding a star! ❤️

Join us on Discord:  
<a href="https://discord.gg/JeXhcmjZVm">
<img alt="discord-invite" src="https://dcbadge.vercel.app/api/server/JeXhcmjZVm?style=flat">
</a>

## Install (Docker)
Run the API locally using Docker:
```
docker run -p 8080:8080 -d ghcr.io/substratusai/sentence-transformers-api
```

## Install (Local python)
Install and run the API server locally using Python. Only supports python 3.9, 3.10 and 3.11.

Clone the repo:
```bash
git clone https://github.com/substratusai/sentence-transformers-api
cd sentence-transformers-api
```

Install dependencies:
```bash
pip3 install -r requirements.txt
```

Run the webserver:
```
uvicorn main:app --port 8080 --reload
```

## Usage
Now you can visit the API docs on [http://localhost:8080/docs](http://localhost:8080/docs)

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


## Creators
Feel free to contact any of us:
* [Sam Stoelinga](https://www.linkedin.com/in/samstoelinga/)
* [Nick Stogner](https://www.linkedin.com/in/nstogner/)
