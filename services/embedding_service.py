import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingService:
    async def sort_by_similarity(self, word: str, synonyms: list):
        embeddings = await self.get_embeddings([word] + synonyms)
        input_embedding = embeddings[0]
        synonym_embeddings = embeddings[1:]

        similarities = cosine_similarity(
            [input_embedding], synonym_embeddings
        ).flatten()

        return sorted(
            [{"word": synonym, "similarity_score": float(score)} for synonym, score in zip(synonyms, similarities)],
            key=lambda x: x["similarity_score"],
            reverse=True
        )

    async def get_embeddings(self, words):
        response = openai.Embedding.create(
            engine="text-embedding-ada-002",
            input=words
        )
        return [np.array(item["embedding"]) for item in response["data"]]
