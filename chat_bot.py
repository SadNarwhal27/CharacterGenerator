from openai import OpenAI
import os
from dotenv import load_dotenv

class StoryTeller():
    def __init__(self) -> None:
        load_dotenv()

        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generator(self, system:str, user:str, temperature=1):
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are {system}"},
            {"role": "user", "content": f"Create {user}"}
        ],
        temperature=temperature,
        # frequency_penalty=1.0
        )

        return completion.choices[0].message.content

    def generate_backstory(self, character:dict, lod='one paragraph'):
        system = "an experienced dungeon master from D&D 5e who is adept at building backstories for characters from a given prompt."
        user = f"{lod} npc backstory using the given JSON file of character information: {character}"
        story = self.generator(system, user)

        return story
    
    def generate_item_description(self, item:dict, lod=2):
        levels_of_detail = {
            1: 'simple paragraph',
            2: 'somewhat detailed paragraph',
            3: 'detailed paragraph'
        }
        
        system = "an experienced item describer from D&D 5e who is exceptional at describing items based on given attributes with a value scale of 10GP (mundane items) to 7500GP (grand items)."
        user = f"a {levels_of_detail[lod]} item description using the given JSON file of item information: {item}."
        temperature = 1.2
        description = self.generator(system, user, temperature)
        return description
    
    def generate_item_name(self, item:dict, lod=2):
        system = "an experienced item namer from D&D 5e who is exceptional at naming items based on given attributes with a value scale of 10GP (mundane items) to 7500GP (grand items)"
        user = f"just an item name using the given JSON file of item information: {item}. Make sure to include the original treasure name in the new item name."
        temperature = 1.2
        name = self.generator(system, user, temperature)
        return name

if __name__ == '__main__':
    from CardBuilder import CardTemplates
    card = CardTemplates().create_NPC()
    # print(StoryTeller().generate_backstory(card, lod='one sentence'))
    # item = {
    #     "treasure_description": "Copper with silver filigree",
    #     "treasure_name": "Chalice",
    #     "treasure_options": None,
    #     "treasure_type": "art object",
    #     "value": 25
    # }
    # print(StoryTeller().generate_item_description(item))