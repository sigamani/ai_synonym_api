"""
Module for a simple v1 implementation of the synonym app.

This module processes a single word by generating synonyms, computing their embeddings,
and returning the synonyms ranked by cosine similarity to the input word.
"""

import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity


class SynonymService:
    def __init__(self):
        """Initialize the SynonymService with OpenAI client and API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    @staticmethod
    async def validate_word(word: str) -> bool:
        """Validates that the input word adheres to rules defined below."""
        if not word.isalpha():
            return False  # Non-alphabetic characters (beyond your current check).
        if len(word) > 50:
            return False  # Words that are excessively long.
        if len(word.split()) > 1:
            return False  # Input cannot contain more than one word.
        return True

    async def generate_synonyms(self, word: str) -> list[str]:
        """Generates synonyms for a given word."""
        if not await self.validate_word(word):
            raise ValueError(f"Invalid word: '{word}'. Please provide a valid word.")

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"You are an expert in linguistics."
                        f"Please provide a list of at least 10 synonyms for "
                        f"the word: '{word}'. Respond only with the required "
                        f"synonyms, separated by: ###."
                    ),
                }
            ],
            model="gpt-4",  # or gpt-3.5-turbo
        )
        synonyms_text = response.choices[0].message.content.strip()
        synonyms = synonyms_text.split("###")
        return [s.strip() for s in synonyms if s.strip()]


class EmbeddingService:
    def __init__(self):
        """Initialize the EmbeddingService with OpenAI client and API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    async def get_embeddings(self, words: list[str]) -> list[list[float]]:
        """Returns embeddings as a for a list of words."""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002", input=words
        )
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
