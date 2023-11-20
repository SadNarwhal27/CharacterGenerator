from DataGrabber import DataGrabber
from CardAssistant import CardAssistant
from chat_bot import StoryTeller
import json

class CardTemplates():
    def __init__(self):
        self.grabber = DataGrabber()
        self.card_assistant = CardAssistant()
        self.story_teller = StoryTeller()
    
    def create_NPC(self, data_filters=None):
        data_filters = self.card_assistant.data_filter_checker(data_filters)
        create_backstory = data_filters.pop('backstory')

        card = dict(self.grabber.get_data('character_first_names', data_filters))
        card.update(self.grabber.get_data('races', {'race': card['race']}))

        card.update(self.grabber.get_data('occupations'))
        card.update(self.card_assistant.generate_stats(-2, 2))
        card.update(self.card_assistant.generate_ac(10, card['modifiers']['DEX_MOD']))
        card.update(self.card_assistant.generate_hp(1, 8, card['modifiers']['CON_MOD']))
        card.update(self.card_assistant.choose_weapon(card['modifiers']))
        card['senses'] += f" {self.card_assistant.generate_passive_perception(card['modifiers']['WIS_MOD'])}"

        card['alignment'] = self.card_assistant.get_alignment()
        if create_backstory:
            card['backstory'] = self.story_teller.generate_backstory(card)

        return self.grabber.save_to_json(card)
    
if __name__ == '__main__':
    templates = CardTemplates()
    print(json.dumps(templates.create_NPC({'race': 'dwarf', 'gender': 'male'}), indent=4))
