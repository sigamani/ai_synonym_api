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


    async def is_valid_word(self, word: str) -> bool:
        """
        Checks if the input word is valid.

        This is a placeholder.  Replace with your actual validation logic.
        """
        # Placeholder implementation - replace with a real check
        return word.isalpha()