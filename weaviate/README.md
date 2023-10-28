# STAPI Weaviate Tutorial
A short tutorial that shows easy it is to use STAPI
(Sentence Transformers API)
with Weaviate by using the text2vec-openai module.

## Install: Local Docker Compose
Bring up Weaviate and STAPI:
```bash
docker compose up -d
```

Create the schema that vectorizes using STAPI endpoint:
```
curl -X POST \
     -H "Content-Type: application/json" \
     -d @schema.json \
     http://localhost:8080/v1/schema
```

Create an object in Weaviate and watch the embedding magic happen:
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d @object.json \
     http://localhost:8080/v1/objects?consistency_level=ALL
```
