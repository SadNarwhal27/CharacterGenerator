from DataGrabber import DataGrabber
from CardAssistant import CardAssistant

class CardTemplates():
    def __init__(self):
        self.grabber = DataGrabber()
        self.card_assistant = CardAssistant()
    
    def create_NPC(self, data_filters=None):
        if data_filters:
            if 'race' in data_filters.keys():
                picked_race = self.grabber.filter_data(self.card_assistant.race_data, {'race':data_filters['race']})
            else:
                picked_race = self.grabber.pick_something(self.card_assistant.race_data)
                data_filters['race'] = picked_race['race']

            filtered_name_data = self.grabber.filter_data(self.card_assistant.name_data, data_filters)
            card = self.grabber.pick_something(filtered_name_data)
            card.update(picked_race)
        else:
            picked_name = self.grabber.pick_something(self.card_assistant.name_data)
            picked_race = self.grabber.filter_data(self.card_assistant.race_data, {'race':picked_name['race']})[0]
            card = picked_name
            card.update(picked_race)
        
        occupation = self.grabber.pick_something(self.grabber.read_data_from_csv('occupations.csv'))
        card.update(occupation)

        card.update(self.card_assistant.generate_stats(-2, 2))
        card.update(self.card_assistant.generate_ac(10, card['modifiers']['DEX_MOD']))
        card.update(self.card_assistant.generate_hp(1, 8, card['modifiers']['CON_MOD']))
        card.update(self.card_assistant.choose_weapon(card['modifiers']))
        
        passive_perception = self.card_assistant.generate_passive_perception(card['modifiers']['WIS_MOD'])
        card['senses'] += f' {passive_perception}'

        final_card = self.grabber.save_to_json(card)
        return final_card
    
if __name__ == '__main__':
    templates = CardTemplates()
    print(templates.create_NPC())