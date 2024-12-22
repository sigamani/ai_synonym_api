from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_synonyms_endpoint():
    response = client.post("/synonyms", json={"word": "example"})
    assert response.status_code == 200
    assert "input_word" in response.json()
    assert "synonyms" in response.json()


def test_synonyms_empty_input():
    response = client.post("/synonyms", json={"word": ""})
    assert response.status_code == 400
