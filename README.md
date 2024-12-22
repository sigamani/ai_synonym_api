# AI Synonym API

## Description

A scalable API to fetch synonyms for a given word using OpenAI's language models and embedding services.

## Features

- Generate a list of synonyms for an input word.
- Sort synonyms by semantic similarity.
- Designed using FastAPI for efficiency.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repo-url>
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

5. Access API documentation at `http://127.0.0.1:8000/docs`.

## Testing

Run tests with Pytest:

```bash
pytest --cov=app tests/
```

## Docker Deployment

1. Build and run the Docker container:
   ```bash
   docker build -t ai-synonym-api .
   docker run -p 8000:8000 ai-synonym-api
   ```

2. Access the application at `http://127.0.0.1:8000`.

## AWS Deployment

1. Use Terraform to set up CI/CD pipeline and deployment:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```
2. Ensure your AWS credentials are configured using `aws configure`.
