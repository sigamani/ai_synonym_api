import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class SynonymService:
    """Service for generating synonyms using OpenAI."""

    async def generate_synonyms(self, word: str) -> list[str]:
        """Generates synonyms for a given word."""
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Please provide a list of at least 10 synonyms for the word: '{word}'. Respond only with the required synonyms, separated by: ###."}],
            model="gpt-4",  # or gpt-3.5-turbo
        )
        synonyms = response.choices[0].message.content.strip().split("###")
        return [s.strip() for s in synonyms if s.strip()]

    async def check_word_exists(self, word: str) -> bool:  # Example placeholder method
        """Checks if a word exists (replace with your logic)."""
        return True


class EmbeddingService:
    """Service for calculating embeddings and similarity."""

    async def get_embeddings(self, words: list[str]) -> list[list[float]]:
        """Gets embeddings for a list of words."""
        response = client.embeddings.create(model="text-embedding-ada-002", input=words)
        return [item.embedding for item in response.data]

    async def sort_by_similarity(self, word: str, synonyms: list[str]) -> list[dict]:
        """Sorts synonyms by similarity to the input word."""
        embeddings = await self.get_embeddings([word] + synonyms)
        input_embedding = embeddings[0]
        synonym_embeddings = embeddings[1:]

        similarities = cosine_similarity([input_embedding], synonym_embeddings).flatten()

        return sorted(
            [{"word": synonym, "similarity_score": float(score)} for synonym, score in zip(synonyms, similarities)],
            key=lambda x: x["similarity_score"],
            reverse=True,
        )


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

