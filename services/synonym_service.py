# services/synonym_service.py
"""Module containing the SynonymService class."""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class SynonymService:
    """Service for generating synonyms using OpenAI."""

    async def generate_synonyms(self, word: str) -> list[str]:
        """Generates synonyms for a given word."""
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Please provide a list of at least 10 synonyms for the word: '{word}'. Respond only with the required synonyms, separated by: ###."}],  # Corrected f-string formatting
            model="gpt-4",  # or gpt-3.5-turbo
        )
        synonyms = response.choices[0].message.content.strip().split("###")
        return [s.strip() for s in synonyms if s.strip()]

    async def check_word_exists(self, word: str) -> bool:
        """Checks if a word exists (replace with your logic)."""
        return True
