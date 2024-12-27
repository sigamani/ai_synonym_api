# AI Synonym API

The AI Synonym API is a FastAPI-based application that generates a ranked list of synonyms for a given input word. It leverages OpenAI's GPT-4 to generate synonyms and ranks them by embedding similarity using OpenAI's embedding model.

## Features
- Generate 10 synonyms for any valid input word using OpenAI GPT-4.
- Rank synonyms based on their semantic similarity to the input word using cosine similarity of embeddings.
- Provides a clean and user-friendly RESTful API.
- Robust error handling for invalid inputs and API failures.
- Asynchronous processing for high performance.

---

## Installation

### Prerequisites
- Python 3.11 or above
- OpenAI API key (required for GPT-4 and embeddings)

### Clone the Repository
```bash
git clone https://github.com/sigamani/ai_synonym_api.git
cd ai_synonym_api
