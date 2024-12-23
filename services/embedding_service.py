import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class EmbeddingService:
    """Service for calculating embeddings and similarity."""

    async def get_embeddings(self, words: list[str]) -> list[list[float]]:
        """Returns embeddings as a for a list of words."""
        response = client.embeddings.create(model="text-embedding-ada-002", input=words)
        return [item.embedding for item in response.data]

    async def sort_by_similarity(self, word: str, synonyms: list[str]) -> list[dict]:
        """Sorts synonyms by similarity to the input word."""

        embeddings = await self.get_embeddings([word] + synonyms)
        input_embedding = embeddings[0]
        synonym_embeddings = embeddings[1:]

        similarities = cosine_similarity(
            [input_embedding], synonym_embeddings
        ).flatten()

        return sorted(
            [
                {"word": synonym, "similarity_score": float(score)}
                for synonym, score in zip(synonyms, similarities)
            ],
            key=lambda x: x["similarity_score"],
            reverse=True,
        )
