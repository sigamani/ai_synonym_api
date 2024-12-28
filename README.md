# AI Synonym API

The AI Synonym API is a FastAPI-based application that generates a ranked list of synonyms for a given input word. It leverages OpenAI's GPT-4 to generate synonyms and ranks them by embedding similarity using OpenAI's embedding model.

## Features
- Generate 10 synonyms for any valid input word using OpenAI GPT-4.
- Rank synonyms based on their semantic similarity to the input word using cosine similarity of embeddings.
- Provides a clean and user-friendly RESTful API.
- Error handling for invalid inputs and API failures.
- Asynchronous processing for high performance.
---

## Installation

### Prerequisites
- Python 3.11
- OpenAI API key (required for GPT-4 and embeddings)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/sigamani/ai_synonym_api.git
   cd ai_synonym_api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your_api_key"
   ```

4. Run the application locally:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Use the following curl command to test:
   ```bash
   curl -X POST \
   'http://127.0.0.1:8000/synonyms' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{"word": "happy"}'
   ```
   
7. Access API documentation at `http://127.0.0.1:8000/docs`.

## Testing

Run tests with Pytest:

```bash
pytest --disable-warnings
```

## Deployment

1. Build and run the Docker container:
   ```bash
   docker build -t ai-synonym-api .
   docker run ai_synonym_api 
   ```

2. Access the application at `http://127.0.0.1:8000`.

3. Test deployment set-up can be seen here: [Heroku Deployment](https://ai-synonym-api-183624b326d2.herokuapp.com/))
