import pytest
from services.embedding_service import EmbeddingService
from services.synonym_service import SynonymService


# ... your test functions

@pytest.mark.asyncio
async def test_generate_synonyms():
    service = SynonymService()
    synonyms = await service.generate_synonyms("example")
    assert len(synonyms) == 10


@pytest.mark.asyncio
async def test_sort_by_similarity():
    service = EmbeddingService()
    result = await service.sort_by_similarity("example", ["test", "sample"])
    assert isinstance(result, list)
