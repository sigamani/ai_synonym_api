from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#from services.synonym_service import SynonymService
#from services.embedding_service import EmbeddingService

###
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class SynonymService:
    async def generate_synonyms(self, word: str):
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a list of at least 10 synonyms for the word: '{word}'."
                               f"Respond only with the required synonyms, separated by: ###. "


                }
            ],
            model="gpt-4o",
        )
        synonyms = response.choices[0].message.content.strip().split("###")
        return synonyms
###

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingService:
    async def sort_by_similarity(self, word: str, synonyms: list):
        embeddings = await self.get_embeddings([word] + synonyms)
        input_embedding = embeddings[0]
        synonym_embeddings = embeddings[1:]

        similarities = cosine_similarity(
            [input_embedding], synonym_embeddings
        ).flatten()

        return sorted(
            [{"word": synonym, "similarity_score": float(score)} for synonym, score in zip(synonyms, similarities)],
            key=lambda x: x["similarity_score"],
            reverse=True
        )

    async def get_embeddings(self, words):
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=words
        )
        embeddings = [item.embedding for item in response.data]
        return embeddings

###

app = FastAPI()

synonym_service = SynonymService()
embedding_service = EmbeddingService()

class WordRequest(BaseModel):
    word: str

class SynonymResponse(BaseModel):
    input_word: str
    synonyms: list


@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(request: WordRequest):
    input_word = request.word.strip()
    if not input_word:
        raise HTTPException(status_code=400, detail="Input word cannot be empty.")

    synonyms = await synonym_service.generate_synonyms(input_word)
    sorted_synonyms = await embedding_service.sort_by_similarity(input_word, synonyms)
    return SynonymResponse(input_word=input_word, synonyms=sorted_synonyms)
