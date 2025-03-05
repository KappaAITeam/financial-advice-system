from fastapi import APIRouter
from src.api.models.embedding import EmbeddingRequest, EmbeddingResponse

router = APIRouter()


@router.post("/embed")
async def embed_text(request: EmbeddingRequest):
    return {"message": "Embedding logic goes here"}
