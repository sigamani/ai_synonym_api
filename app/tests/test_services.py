"""
Unit tests for the SynonymService class in services.synonym_service.
"""

import pytest
from services.synonym_service import SynonymService

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
    """Test validate_word with a non-alphabetic string.
       This could be functionality we want to account
       for to deal with Brand entities for example (e.g. Audi A4)"""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("hello123")
    assert result is False


@pytest.mark.asyncio
async def test_validate_word_excessive_length():
    """Test validate_word with a word that exceeds the maximum length."""
    synonym_service = SynonymService()
    result = await synonym_service.validate_word("a" * 51)
    assert result is False



