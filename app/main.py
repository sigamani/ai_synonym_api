"""
Main module for the AI Synonym API using FastAPI.
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from services.synonym_service import SynonymService

app = FastAPI()


class SynonymRequest(BaseModel):
    """
    Request model for synonym generation.
    """

    word: str


class SynonymResponse(BaseModel):
    """
    Response model for synonym generation.
    """

    word: str
    synonyms: List[str]


def get_synonym_service():
    """
    Dependency injection for SynonymService.
    """
    return SynonymService()


@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(
    request: SynonymRequest,
    synonym_service: SynonymService = Depends(get_synonym_service),
):
    """
    Endpoint to get synonyms for a given word.
    """
    is_valid = await synonym_service.validate_word(request.word)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid word input.")
    try:
        synonyms = await synonym_service.generate_synonyms(request.word)
        return SynonymResponse(word=request.word, synonyms=synonyms)
    except ValueError as error:
        raise HTTPException(status_code=500, detail="Internal server error") from error
