# services/synonym_service.py
"""Module containing the SynonymService class."""

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class SynonymService:
    """Service for generating synonyms using OpenAI."""
    def __init__(self):
        print("Initializing SynonymService")

    async def generate_synonyms(self, word: str) -> list[str]:
        """Generates synonyms for a given word."""

        if not await self.validate_word(word):
            raise ValueError(f"Invalid word: '{word}'. Please provide a valid word.")

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": (
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


    async def validate_word(self, word: str) -> bool:
        """Sense check for the input word."""
        if not word:
            return False  # Empty strings or null inputs.
        if not word.isalpha():
            return False  # Non-alphabetic characters (beyond your current check).
        if len(word) > 50:
            return False  # Words that are excessively long.
        return True