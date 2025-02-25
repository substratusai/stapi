from typing import Union, List, Dict, Optional
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

models: Dict[str, SentenceTransformer] = {}
model_name = os.getenv("MODEL", "all-MiniLM-L6-v2")
api_key = os.getenv("API_KEY")

security = HTTPBearer(auto_error=False)

def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    if api_key:
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="API key required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if credentials.credentials != api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials.credentials
    return None


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]] = Field(
        examples=["substratus.ai provides the best LLM tools"]
    )
    model: str = Field(
        examples=[model_name],
        default=model_name,
    )


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
    models[model_name] = SentenceTransformer(model_name, trust_remote_code=True)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/v1/embeddings")
async def embedding(
    item: EmbeddingRequest,
    api_key: Optional[str] = Depends(verify_api_key)
) -> EmbeddingResponse:
    model: SentenceTransformer = models[model_name]
    if isinstance(item.input, str):
        vectors = model.encode(item.input)
        tokens = len(vectors)
        return EmbeddingResponse(
            data=[EmbeddingData(embedding=vectors, index=0, object="embedding")],
            model=model_name,
            usage=Usage(prompt_tokens=tokens, total_tokens=tokens),
            object="list",
        )
    if isinstance(item.input, list):
        embeddings = []
        tokens = 0
        for index, text_input in enumerate(item.input):
            if not isinstance(text_input, str):
                raise HTTPException(
                    status_code=400,
                    detail="input needs to be an array of strings or a string",
                )
            vectors = model.encode(text_input)
            tokens += len(vectors)
            embeddings.append(
                EmbeddingData(embedding=vectors, index=index, object="embedding")
            )
        return EmbeddingResponse(
            data=embeddings,
            model=model_name,
            usage=Usage(prompt_tokens=tokens, total_tokens=tokens),
            object="list",
        )
    raise HTTPException(
        status_code=400, detail="input needs to be an array of strings or a string"
    )


@app.get("/")
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
