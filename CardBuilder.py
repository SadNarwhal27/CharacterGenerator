from DataGrabber import DataGrabber
from CardAssistant import CardAssistant
from chat_bot import StoryTeller
import json, random

class CardTemplates():
    def __init__(self):
        self.grabber = DataGrabber()
        self.card_assistant = CardAssistant()
        self.story_teller = StoryTeller()
    
    def create_NPC(self, data_filters:dict=None):
        """Used to create NPC cards"""

        # Validates filters
        data_filters = self.card_assistant.data_filter_checker(data_filters)
        
        # Checks if a backstory is requested to save chat bot cycles. Might just make this a default eventually.
        if data_filters:
            create_backstory = data_filters.pop('backstory')
        else:
            create_backstory = None

        # Initializes the card and fills in data
        card = dict(self.grabber.get_line('first_names', data_filters))
        card.update(self.grabber.get_line('races', {'race': card['race']}))

        card.update(self.card_assistant.generate_stats(-2, 2))

        card.update(self.grabber.get_line('occupations'))
        card['skills'] = self.card_assistant.generate_skills(card['skills'], card['modifiers'])

        card.update(self.card_assistant.generate_ac(10, card['modifiers']['DEX_MOD']))

        card.update(self.card_assistant.generate_hp(1, 8, card['modifiers']['CON_MOD']))
        if card['hp'] < 4:
            card['hp'] = 4

        card.update(self.card_assistant.choose_weapon(card['modifiers']))
        card['senses'] += f" {self.card_assistant.generate_passive_perception(card['modifiers']['WIS_MOD'])}"

        card['alignment'] = self.card_assistant.get_alignment()
        
        # Uses the chat bot to create a backstory
        if create_backstory:
            card['backstory'] = self.story_teller.generate_backstory(card)

        return card
    
    # Will probably granularize this into just treasure
    def create_item(self, data_filters:dict=None):
        """Used to create item cards."""

        # Filters treasure type if filter is given
        if data_filters['type'] and data_filters['type'] != 'None':
            card = dict(self.grabber.get_line('treasure', {'treasure_type': data_filters['type']}))
        else:
            card = dict(self.grabber.get_line('treasure'))
        
        # Adds the gold piece (GP) to each value
        card['value'] = str(card['value']) + 'GP'

        # Picks a treasure option and adds it to the description
        if card['treasure_options']:
            options = card['treasure_options'].split(',')
            card['treasure_description'] = card['treasure_description'].replace('<>', random.choice(options))
        card.pop('treasure_options')

        # Creates an interesting name if the treasure is an art object
        if card['treasure_type'] == 'art object':
            card['treasure_name'] = self.story_teller.generate_item_name(card)

        if data_filters['lod'] == 'None':
            data_filters['lod'] = 2
        
        # Generates an item description using the chat bot
        card['generated_description'] = self.story_teller.generate_item_description(card, int(data_filters['lod']))

        return card
    
    def create_spell(self, data_filters:dict=None):
        spells = self.grabber.get_data('spells', data_filters)

        if data_filters['spell_name'] != 'None':
            card = spells[data_filters['spell_name']]
            return card
        else:
            card = spells
        
        if data_filters['spell_classes'] != 'None':
            card['filter_class'] = data_filters['spell_classes']
        else:
            card['filter_class'] = 'any'

        return spells

if __name__ == '__main__':
    templates = CardTemplates()
    print(json.dumps(templates.create_NPC({'race': 'dwarf', 'gender': 'male'}), indent=4))
