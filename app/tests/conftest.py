"""
Configuration for testing the Synonym API.

Includes dependency overrides for SynonymService and EmbeddingService.
"""

import pytest
from services.synonym_service_v1 import SynonymService, EmbeddingService


class MockSynonymService(SynonymService):
    """Mocked implementation of SynonymService."""
    async def validate_word(self, word):
        return True

    async def generate_synonyms(self, word):
        return ["happy", "joyful", "cheerful"]


class MockEmbeddingService(EmbeddingService):
    """Mocked implementation of EmbeddingService."""
    async def sort_by_similarity(self, word, synonyms):
        return [{"word": synonym, "similarity_score": 0.99} for synonym in synonyms]


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    """Override dependencies with mock services."""
    monkeypatch.setattr("app.main.get_synonym_service", lambda: MockSynonymService())
    monkeypatch.setattr("app.main.get_embedding_service", lambda: MockEmbeddingService())