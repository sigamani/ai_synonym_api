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
        return [{"word": synonym, "similarity_score": 0.99} for synonym in synonyms]


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
