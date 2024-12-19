from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_synonyms_endpoint():
    response = client.post("/synonyms", json={"word": "example"})
    assert response.status_code == 200
    assert "input_word" in response.json()
    assert "synonyms" in response.json()

def test_synonyms_empty_input():
    response = client.post("/synonyms", json={"word": ""})
    assert response.status_code == 400

# File: app/tests/test_services.py
from app.services.synonym_service import SynonymService
from app.services.embedding_service import EmbeddingService

import pytest
import numpy as np

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
