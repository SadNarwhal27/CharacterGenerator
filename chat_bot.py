from openai import OpenAI
import os
from dotenv import load_dotenv

class StoryTeller():
    def __init__(self) -> None:
        load_dotenv()

        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_backstory(self, character):
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a experienced dungeon master from D&D 5e who is adept at building backstories for characters from a given prompt."},
            {"role": "user", "content": f"Create a one paragraph npc backstory using the given JSON file of character information: {character}"}
        ],
        temperature=0.5,
        )

        return completion.choices[0].message.content
