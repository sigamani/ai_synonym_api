import openai

class SynonymService:
    async def generate_synonyms(self, word: str):
        prompt = f"Generate a list of 10 synonyms for the word '{word}'."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        synonyms = response.choices[0].text.strip().split(",")
        return [s.strip() for s in synonyms]
