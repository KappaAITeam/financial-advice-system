# src/api/models/embedding.py
from pydantic import BaseModel
from typing import List


class EmbeddingRequest(BaseModel):
    """
    Model for requesting a text to be embedded.
    """
    text: str


class EmbeddingResponse(BaseModel):
    """
    Model representing the embedding of a text.
    """
    vector_id: str            # Unique ID for the stored vector
    embedding: List[float]      # List of floats representing the vector
