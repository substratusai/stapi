from typing import Union, List
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer



class EmbeddingRequest(BaseModel):
    input: str | List[str]
    model: str

class EmbeddingData(BaseModel):
    embedding: List[float]
    index: int
    object: str

class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int

class EmbeddingResponse(BaseModel):
    data: List[EmbeddingData]
    model: str
    usage: Usage
    object: str


models = {}
model_name = 'all-MiniLM-L6-v2'


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["default"] = SentenceTransformer(model_name)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/v1/embeddings")
async def embedding(item: EmbeddingRequest) -> EmbeddingResponse:
    if isinstance(item.input, str):
        vectors = models["default"].encode(item.input)
        tokens = len(vectors)
        return EmbeddingResponse(
            data=[EmbeddingData(embedding=vectors, index=0, object="embedding")],
            model=model_name,
            usage=Usage(prompt_tokens=tokens, total_tokens=tokens),
            object="list"
        )
