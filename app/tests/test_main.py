"""
Unit tests for the Synonym API endpoints in app.main.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_synonyms_endpoint_invalid_word():
    """Test the /synonyms endpoint with an invalid word."""
    response = client.post("/synonyms", json={"word": "1234"})
    assert response.status_code == 400


def test_synonyms_service_openai_error(monkeypatch):
    """Test the /synonyms endpoint when OpenAI API raises an error."""

    class ErrorMockService:
        async def validate_word(self, word):
            return True

        async def generate_synonyms(self, word):
            raise ValueError("OpenAI API error")

    monkeypatch.setattr("app.main.get_synonym_service", lambda: ErrorMockService())

    response = client.post("/synonyms", json={"word": "happy"})
    assert response.status_code == 500
