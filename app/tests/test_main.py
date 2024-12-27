"""
Unit tests for the FastAPI application in app.main.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_synonym_service
from services.synonym_service import SynonymService

client = TestClient(app)


class MockSynonymService:
    """
    Mocked SynonymService for testing purposes.
    """

    async def validate_word(self, word: str) -> bool:
        return True

    async def generate_synonyms(self, word: str):
        return ["happy", "joyful", "elated"]


def override_get_synonym_service():
    return MockSynonymService()


@pytest.fixture(autouse=True)
def apply_monkeypatch(monkeypatch):
    """
    Fixture to override the SynonymService dependency.
    """
    app.dependency_overrides[get_synonym_service] = override_get_synonym_service
    yield
    app.dependency_overrides.clear()


def test_get_synonyms_valid_word():
    """
    Test /synonyms endpoint with a valid word.
    """
    response = client.post("/synonyms", json={"word": "example"})
    assert response.status_code == 200
    assert response.json() == {
        "word": "example",
        "synonyms": ["happy", "joyful", "elated"],
    }


def test_get_synonyms_invalid_word():
    """
    Test /synonyms endpoint with an invalid word.
    """

    class InvalidWordMockService(MockSynonymService):
        async def validate_word(self, word: str) -> bool:
            return False

    app.dependency_overrides[get_synonym_service] = lambda: InvalidWordMockService()

    response = client.post("/synonyms", json={"word": "1234"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid word input."}


def test_get_synonyms_internal_error():
    """
    Test /synonyms endpoint when generate_synonyms raises an error.
    """

    class ErrorMockService(MockSynonymService):
        async def generate_synonyms(self, word: str):
            raise ValueError("Internal error")

    app.dependency_overrides[get_synonym_service] = lambda: ErrorMockService()

    response = client.post("/synonyms", json={"word": "example"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
