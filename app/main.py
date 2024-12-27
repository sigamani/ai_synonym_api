"""
Main module for the Synonym API using FastAPI.

This API accepts a single word, generates synonyms using SynonymService,
computes their embeddings using EmbeddingService, and ranks the synonyms
based on cosine similarity to the input word.
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from services.synonym_service_v1 import SynonymService, EmbeddingService

app = FastAPI()


class SynonymRequest(BaseModel):
    """Request model for generating synonyms."""

    word: str


class SynonymResponse(BaseModel):
    """Response model for returning ranked synonyms."""

    input_word: str
    synonyms: List[dict]


def get_synonym_service() -> SynonymService:
    """Dependency injection for SynonymService."""
    return SynonymService()


def get_embedding_service() -> EmbeddingService:
    """Dependency injection for EmbeddingService."""
    return EmbeddingService()


@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(
    request: SynonymRequest,
    synonym_service: SynonymService = Depends(get_synonym_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
):
    """
    Endpoint to generate and rank synonyms for a given word.
    """
    input_word = request.word.strip().lower()

    if not input_word:
        raise HTTPException(status_code=400, detail="Input word cannot be empty.")

    try:
        await synonym_service.validate_word(input_word)
        synonyms = await synonym_service.generate_synonyms(input_word)
        ranked_synonyms = await embedding_service.sort_by_similarity(
            input_word, synonyms
        )
        return SynonymResponse(input_word=input_word, synonyms=ranked_synonyms)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal server error") from error
