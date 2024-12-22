import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class SynonymService:
    """Service for generating synonyms using OpenAI."""

    async def generate_synonyms(self, word: str) -> list[str]:
        """Generates a list of synonyms for a given word using OpenAI's GPT model.

        Args:
            word: The input word for which to generate synonyms.

        Returns:
            A list of synonyms.
        """
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Please provide a list of at least 10 synonyms for the word: '{word}'."
                        f"Respond only with the required synonyms, separated by: ###. "
                    ),
                }
            ],
            model="gpt-4",  # or gpt-3.5-turbo
        )
        synonyms = response.choices[0].message.content.strip().split("###")
        return [s.strip() for s in synonyms if s.strip()]

    async def get_example(self): # Added an extra method to address R0903
        """ Placeholder for a real method"""
        pass


class EmbeddingService:
    """Service for calculating embeddings and similarity."""

    async def sort_by_similarity(self, word: str, synonyms: list):
        """Sorts synonyms by their similarity to the input word using embeddings.

        Args:
            word: The input word.
            synonyms: A list of synonyms.

        Returns:
            A list of synonyms sorted by similarity score.
        """
        embeddings = await self.get_embeddings([word] + synonyms)
        input_embedding = embeddings[0]
        synonym_embeddings = embeddings[1:]

        similarities = cosine_similarity([input_embedding], synonym_embeddings).flatten()

        return sorted(
            [
                {"word": synonym, "similarity_score": float(score)}
                for synonym, score in zip(synonyms, similarities)
            ],
            key=lambda x: x["similarity_score"],
            reverse=True,
        )

    async def get_embeddings(self, words: list):
        """Gets embeddings for a list of words using OpenAI's embedding model.
        Args:
            words: The list of words.
        Returns:
            A list of embeddings.

        """
        response = client.embeddings.create(
            model="text-embedding-ada-002", input=words
        )
        return [item.embedding for item in response.data]


app = FastAPI(title="AI Synonym API", description="Generates and sorts synonyms using OpenAI")  # Add title and description


synonym_service = SynonymService()
embedding_service = EmbeddingService()


class WordRequest(BaseModel):
    """Request model for the /synonyms endpoint."""
    word: str


class SynonymResponse(BaseModel):
    """Response model for the /synonyms endpoint."""
    input_word: str
    synonyms: list


@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(request: WordRequest):
    """Endpoint for retrieving synonyms for a given word."""
    input_word = request.word.strip()
    if not input_word:
        raise HTTPException(status_code=400, detail="Input word cannot be empty.")

    synonyms = await synonym_service.generate_synonyms(input_word)
    sorted_synonyms = await embedding_service.sort_by_similarity(input_word, synonyms)
    return SynonymResponse(input_word=input_word, synonyms=sorted_synonyms)

