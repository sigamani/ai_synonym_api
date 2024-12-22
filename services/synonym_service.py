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
