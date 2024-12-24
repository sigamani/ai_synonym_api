import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app
from services.synonym_service import SynonymService

# TestClient setup
client = TestClient(app)


# Mock SynonymService
@pytest.fixture
def mock_synonym_service(monkeypatch):
    """Fixture to mock SynonymService methods."""
    mock_service = SynonymService()
    mock_service.validate_word = AsyncMock()
    mock_service.generate_synonyms = AsyncMock()
    monkeypatch.setattr("app.main.synonym_service", mock_service)
    return mock_service


@pytest.mark.asyncio
async def test_get_synonyms_valid_word(mock_synonym_service):
    """Test /synonyms/{word} endpoint with a valid word."""
    mock_synonym_service.validate_word.return_value = True
    mock_synonym_service.generate_synonyms.return_value = ["happy", "joyful", "elated"]

    response = client.get("/synonyms/example")
    assert response.status_code == 200
    assert response.json() == {"synonyms": ["happy", "joyful", "elated"]}
    mock_synonym_service.validate_word.assert_called_once_with("example")
    mock_synonym_service.generate_synonyms.assert_called_once_with("example")


@pytest.mark.asyncio
async def test_get_synonyms_invalid_word(mock_synonym_service):
    """Test /synonyms/{word} endpoint with an invalid word."""
    mock_synonym_service.validate_word.return_value = False

    response = client.get("/synonyms/1234")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid word"}
    mock_synonym_service.validate_word.assert_called_once_with("1234")
    mock_synonym_service.generate_synonyms.assert_not_called()


@pytest.mark.asyncio
async def test_get_synonyms_empty_word(mock_synonym_service):
    """Test /synonyms/{word} endpoint with an empty word."""
    mock_synonym_service.validate_word.return_value = False

    response = client.get("/synonyms/")
    assert response.status_code == 404  # FastAPI raises a 404 for missing path params


@pytest.mark.asyncio
async def test_get_synonyms_internal_error(mock_synonym_service):
    """Test /synonyms/{word} endpoint when generate_synonyms raises an error."""
    mock_synonym_service.validate_word.return_value = True
    mock_synonym_service.generate_synonyms.side_effect = Exception("Internal error")

    response = client.get("/synonyms/example")
    assert response.status_code == 500
    assert "Internal server error" in response.text
