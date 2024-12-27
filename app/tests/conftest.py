import pytest


@pytest.fixture(autouse=True)
def set_dummy_openai_key(monkeypatch):
    """Automatically set a dummy OPENAI_API_KEY environment variable for all tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")


from services.synonym_service_v1 import SynonymService, EmbeddingService


class MockSynonymService(SynonymService):
    async def validate_word(self, word):
        return True

    async def generate_synonyms(self, word):
        if not word.isalpha():
            raise ValueError("Invalid word: must be alphabetic.")
        return ["happy", "joyful", "cheerful"]


class MockEmbeddingService(EmbeddingService):
    async def sort_by_similarity(self, word, synonyms):
        return [{"word": synonym, "similarity_score": 0.99} for synonym in synonyms]


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    """Override SynonymService and EmbeddingService for tests."""
    monkeypatch.setattr("app.main.get_synonym_service", lambda: MockSynonymService())
    monkeypatch.setattr(
        "app.main.get_embedding_service", lambda: MockEmbeddingService()
    )
