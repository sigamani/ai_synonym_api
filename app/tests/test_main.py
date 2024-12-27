import pytest
from fastapi.testclient import TestClient
from app.main import app, get_synonym_service, get_embedding_service

client = TestClient(app)

# Mock services
class MockSynonymService:
    async def validate_word(self, word):
        return True

    async def generate_synonyms(self, word):
        return ["happy", "joyful", "cheerful"]

class MockEmbeddingService:
    async def sort_by_similarity(self, word, synonyms):
        return [
            {"word": synonym, "similarity_score": 0.99} for synonym in synonyms
        ]

# Dependency overrides
app.dependency_overrides[get_synonym_service] = lambda: MockSynonymService()
app.dependency_overrides[get_embedding_service] = lambda: MockEmbeddingService()

def test_synonyms_endpoint_valid_word():
    """
    Test the /synonyms endpoint with a valid word.
    """
    response = client.post("/synonyms", json={"word": "happy"})
    assert response.status_code == 200
    expected_response = {
        "input_word": "happy",
        "synonyms": [
            {"word": "happy", "similarity_score": 0.99},
            {"word": "joyful", "similarity_score": 0.99},
            {"word": "cheerful", "similarity_score": 0.99},
        ],
    }
    assert response.json() == expected_response


def test_synonyms_endpoint_empty_word():
    """
    Test the /synonyms endpoint with an empty word.
    """
    response = client.post("/synonyms", json={"word": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Input word cannot be empty."


def test_synonyms_endpoint_invalid_word():
    """
    Test the /synonyms endpoint with an invalid word (e.g., non-alphabetic).
    """
    response = client.post("/synonyms", json={"word": "1234"})
    assert response.status_code == 400
    assert "Invalid word" in response.json()["detail"]


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    """
    Test SynonymService when the API key is missing.
    """
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from services.synonym_service_v1 import SynonymService

    with pytest.raises(EnvironmentError, match="Missing OPENAI_API_KEY environment variable."):
        SynonymService()


def test_synonyms_service_openai_error(monkeypatch):
    """
    Test the /synonyms endpoint when OpenAI API raises an error.
    """
    class ErrorMockService:
        async def validate_word(self, word):
            return True

        async def generate_synonyms(self, word):
            raise ValueError("OpenAI API error")

    monkeypatch.setattr("app.main.get_synonym_service", lambda: ErrorMockService())

    response = client.post("/synonyms", json={"word": "happy"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"