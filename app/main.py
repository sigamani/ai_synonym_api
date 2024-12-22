import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from services.embedding_service import EmbeddingService # import directly rather than defining a class with same name in main.py.
from services.synonym_service import SynonymService

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI(title="AI Synonym API", description="Generates and sorts synonyms using OpenAI")

synonym_service = SynonymService()
embedding_service = EmbeddingService()


class WordRequest(BaseModel):
    """Request model for the /synonyms endpoint."""

    word: str


class SynonymResponse(BaseModel):
    """Response model for the /synonyms endpoint."""

    input_word: str
    synonyms: list[dict]


@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(request: WordRequest) -> SynonymResponse:
    """Endpoint for retrieving synonyms for a given word."""
    input_word = request.word.strip()
    if not input_word:
        raise HTTPException(status_code=400, detail="Input word cannot be empty.")

    synonyms = await synonym_service.generate_synonyms(input_word)
    sorted_synonyms = await embedding_service.sort_by_similarity(input_word, synonyms)
    return SynonymResponse(input_word=input_word, synonyms=sorted_synonyms)