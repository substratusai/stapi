from typing import Union, List, Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

models: Dict[str, SentenceTransformer] = {}
default_model_name = 'all-MiniLM-L6-v2'

class EmbeddingRequest(BaseModel):
    input: str | List[str] = Field(examples=["substratus.ai provides the best LLM tools"])
    model: str = Field(examples=[default_model_name], default=default_model_name)

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    models[default_model_name] = SentenceTransformer(default_model_name)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/v1/embeddings")
async def embedding(item: EmbeddingRequest) -> EmbeddingResponse:
    selected_model: SentenceTransformer = models.setdefault(item.model, SentenceTransformer(item.model))
    if isinstance(item.input, str):
        vectors = selected_model.encode(item.input)
        tokens = len(vectors)
        return EmbeddingResponse(
            data=[EmbeddingData(embedding=vectors, index=0, object="embedding")],
            model=item.model,
            usage=Usage(prompt_tokens=tokens, total_tokens=tokens),
            object="list"
        )
    if isinstance(item.input, list):
        embeddings = []
        tokens = 0
        for index, text_input in enumerate(item.input):
            if not isinstance(text_input, str):
                raise HTTPException(status_code=400, detail="input needs to be an array of strings or a string")
            vectors = models["default"].encode(item.input)
            tokens += len(vectors)
            embeddings.append(EmbeddingData(embedding=vectors, index=index, object="embedding"))
        return EmbeddingResponse(
            data=embeddings,
            model=item.model,
            usage=Usage(prompt_tokens=tokens, total_tokens=tokens),
            object="list"
        )
    raise HTTPException(status_code=400, detail="input needs to be an array of strings or a string")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
