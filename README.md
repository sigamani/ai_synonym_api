# AI Synonym API

The AI Synonym API is a FastAPI-based application that generates a ranked list of synonyms for a given input word. It leverages OpenAI's GPT-4 to generate synonyms and ranks them by embedding similarity using OpenAI's embedding model.

## Features
- Generate 10 synonyms for any valid input word using OpenAI GPT-4.
- Rank synonyms based on their semantic similarity to the input word using cosine similarity of embeddings.
- Provides a clean and user-friendly RESTful API.
- Error handling for invalid inputs and API failures.
- Asynchronous processing for high performance.

## Future Improvements and To-Do List

If given more time, the following improvements and features would be implemented to enhance the project:

1. **Evaluation Dataset**: 
   - Create a robust evaluation dataset to serve as a ground truth for benchmarking the current model's performance and tracking improvements over time.

2. **Define Accuracy Metrics**: 
   - Establish clear metrics for evaluation, such as precision, recall, and F1 score.
   - Utilize tools like [Thesaurus.com](https://www.thesaurus.com) to identify the strongest matches for comparison.

3. **Embedding Experiments**: 
   - Test different embedding models, including domain-specific embeddings, to optimise results.

4. **Embedding Caching**: 
   - Implement a caching mechanism to store embedding vectors in a database, enabling faster retrieval and reducing API costs and calls to OpenAI.

5. **Disambiguation Module**: 
   - Develop a module to handle ambiguous words (e.g., `bat` as a noun for a mammal vs. a sports implement, or as a verb).

6. **LangChain Integration**: 
   - Incorporate [LangChain](https://www.langchain.com) for efficient LLM operations and workflows.

7. **Guardrails for Responses**: 
   - Add safety measures to prevent inappropriate or unintended responses from the model.

8. **Advanced Prompting Techniques**: 
   - Experiment with different prompting strategies, such as few-shot learning with carefully curated examples, to reduce ambiguity and improve model clarity.

9. **LangSmith Integration**: 
   - Leverage [LangSmith](https://docs.langsmith.com/) to track and analyse prompting accuracy for continuous optimisation.

By addressing these tasks, the project could achieve greater efficiency, accuracy, and scalability while maintaining robustness and user safety.

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

3. Test deployment set-up can be seen here: [Heroku Deployment](https://ai-synonym-api-183624b326d2.herokuapp.com/)
