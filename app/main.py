from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from services.synonym_service import SynonymService
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Dependency injection for services
synonym_service = SynonymService()


# Pydantic models
class SynonymResponse(BaseModel):
    synonyms: List[str] = Field(..., description="List of synonyms for the input word.")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message describing the issue.")


@app.get(
    "/synonyms/{word}",
    response_model=SynonymResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input word."},
        500: {"model": ErrorResponse, "description": "Internal server error."},
    },
)
@app.get(
    "/synonyms/{word}",
    response_model=SynonymResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input word."},
        500: {"model": ErrorResponse, "description": "Internal server error."},
    },
)
async def get_synonyms(word: str):
    if not await synonym_service.validate_word(word):
        raise HTTPException(status_code=400, detail="Invalid word")

    try:
        synonyms = await synonym_service.generate_synonyms(word)
        return SynonymResponse(synonyms=synonyms)
    except Exception as e:
        # Explicitly return a JSON response for 500 errors
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
