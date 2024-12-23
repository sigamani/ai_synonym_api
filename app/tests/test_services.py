import pytest
from services.synonym_service import SynonymService


@pytest.fixture
def synonym_service():
    """Fixture to create an instance of SynonymService."""
    return SynonymService()


@pytest.mark.asyncio
async def test_validate_word_empty_string(synonym_service):
    """Test validate_word with an empty string."""
    word = ""
    result = await synonym_service.validate_word(word)
    assert result is False, "Empty string should be invalid."


@pytest.mark.asyncio
async def test_validate_word_non_alpha(synonym_service):
    """Test validate_word with a non-alphabetic string."""
    word = "hello123"
    result = await synonym_service.validate_word(word)
    assert result is False, "Non-alphabetic string should be invalid."


@pytest.mark.asyncio
async def test_validate_word_excessive_length(synonym_service):
    """Test validate_word with a word that exceeds the maximum length."""
    word = "a" * 51  # 51 characters
    result = await synonym_service.validate_word(word)
    assert result is False, "Word exceeding length limit should be invalid."


@pytest.mark.asyncio
async def test_validate_word_valid(synonym_service):
    """Test validate_word with a valid word."""
    word = "example"
    result = await synonym_service.validate_word(word)
    assert result is True, "Valid word should pass validation."
