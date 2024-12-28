"""
Configuration for testing the Synonym API.

Includes dependency overrides for SynonymService and EmbeddingService.
"""

import pytest
from services.synonym_service_v1 import SynonymService, EmbeddingService


@pytest.fixture(autouse=True)
def set_dummy_openai_key(monkeypatch):
    """Set a dummy OPENAI_API_KEY for tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")


class MockSynonymService(SynonymService):
    """Mock implementation of SynonymService for testing."""

    async def validate_word(self, word: str) -> bool:
        return True

    async def generate_synonyms(self, word):
        return ["happy", "joyful", "cheerful"]


class MockEmbeddingService(EmbeddingService):
    """Mocked implementation of EmbeddingService.
    No longer inherits from SynonymService, so it won’t require OPENAI_API_KEY.
    Update the override_dependencies Fixture"""

    async def sort_by_similarity(self, word, synonyms):
        return [{"word": synonym, "similarity_score": 0.99} for synonym in synonyms]


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    """Override dependencies with mock services."""
    monkeypatch.setattr("app.main.get_synonym_service", lambda: MockSynonymService())
    monkeypatch.setattr(
        "app.main.get_embedding_service", lambda: MockEmbeddingService()
    )
