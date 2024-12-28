"""Unit tests for the SynonymService."""

import pytest
from unittest.mock import MagicMock
from services.synonym_service_v1 import SynonymService, EmbeddingService


@pytest.mark.asyncio
async def test_validate_word_valid():
    """Test validate_word with a valid word."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("example")
    assert result is True


@pytest.mark.asyncio
async def test_validate_word_empty_string():
    """Test validate_word with an empty string."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("")
    assert result is False


@pytest.mark.asyncio
async def test_validate_word_non_alpha():
    """Test validate_word with a non-alphabetic string."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("hello123")
    assert result is False


@pytest.mark.asyncio
async def test_validate_word_excessive_length():
    """Test validate_word with a word that exceeds the maximum length."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("a" * 51)
    assert result is False


@pytest.mark.asyncio
async def test_validate_word_multiple_words():
    """Test validate_word with more than one word."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("hello world")
    assert result is False


@pytest.mark.asyncio
async def test_generate_synonyms_success(mocker):
    # Mock OpenAI client
    mock_client = MagicMock()
    mocker.patch("services.synonym_service_v1.OpenAI", return_value=mock_client)

    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="happy###joyful###content"))]
    )

    service = SynonymService()
    synonyms = await service.generate_synonyms("happy")

    assert synonyms == ["happy", "joyful", "content"]


@pytest.mark.asyncio
async def test_generate_synonyms_validation_failure(mocker):
    mocker.patch(
        "services.synonym_service_v1.SynonymService.validate_word", return_value=False
    )

    service = SynonymService()
    with pytest.raises(ValueError, match="Invalid word: '123happy'"):
        await service.generate_synonyms("123happy")


@pytest.mark.asyncio
async def test_get_embeddings_success(mocker):
    # Mock OpenAI client
    mock_client = MagicMock()
    mocker.patch("services.synonym_service_v1.OpenAI", return_value=mock_client)

    mock_client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2]), MagicMock(embedding=[0.3, 0.4])]
    )

    service = EmbeddingService()
    embeddings = await service.get_embeddings(["happy", "joyful"])

    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]


@pytest.mark.asyncio
async def test_get_embeddings_api_failure(mocker):
    # Mock OpenAI client
    mock_client = MagicMock()
    mocker.patch("services.synonym_service_v1.OpenAI", return_value=mock_client)

    mock_client.embeddings.create.side_effect = Exception("API error")

    service = EmbeddingService()
    with pytest.raises(Exception, match="API error"):
        await service.get_embeddings(["happy", "joyful"])
