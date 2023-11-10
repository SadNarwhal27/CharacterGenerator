from DataGrabber import DataGrabber
import random
import copy
import math

class CardCreator():
    def __init__(self):
        self.grabber = DataGrabber()
        self.base_stats = {"STR": 0,"DEX": 0,"CON": 0,"INT": 0,"WIS": 0,"CHA": 0}

    def create_npc_card(self, data_filters=None):
        name_data = self.grabber.read_data_from_csv('character_names.csv')
        if data_filters:
            filtered_name_data = self.grabber.filter_data(name_data, data_filters)
            card = self.grabber.pick_something(filtered_name_data)
        else:
            card = self.grabber.pick_something(name_data)
        
        occupation = self.grabber.pick_something(self.grabber.read_data_from_csv('occupations.csv'))
        card.update(occupation)

        stats = copy.deepcopy(self.base_stats)
        modifiers = {}
        for key in stats.keys():
            stats[key] = 10 + random.randint(-2, 2) # Add a plus minus range variable
            modifer = math.floor((stats[key] - 10) / 2)

            # modifiers[f'{key}_MOD'] = str(modifer) if modifer < 0 else str(f'+{modifer}')
            modifiers[f'{key}_MOD'] = modifer
        card['stats'] = stats
        card['modifiers'] = modifiers

        card['ac'] = 10 + modifiers['DEX_MOD']
        
        hp = random.randint(1, 8) + modifiers['CON_MOD']
        if hp <= 0:
            hp = 1
        card['hp'] = hp

        return card

if __name__ == '__main__':
    creator = CardCreator()
    filters = {'race':'human', 'gender':'female'}
    print(creator.create_npc_card(filters))