from DataGrabber import DataGrabber
import random
import copy
import math

class CardAssistant():
    def __init__(self):
        self.grabber = DataGrabber()
        self.base_stats = {"STR": 0,"DEX": 0,"CON": 0,"INT": 0,"WIS": 0,"CHA": 0}
        self.alignments = {
            3: ['Chaotic Evil', 'Chaotic Neutral'],
            5: ['Lawful Evil'],
            8: ['Neutral Evil'],
            12: ['Neutral'],
            15: ['Neutral Good'],
            17: ['Lawful Good', 'Lawful Neutral'],
            18: ['Chaotic Good', 'Chaotic Neutral']
            }

    def roll_dice(self, qty, sides, modifier=0):
        """Simulates rolling dice"""
        rolls = []
        for _ in range(qty):
            roll = random.randint(1, sides)
            rolls.append(roll)
        if len(rolls) == 1:
            total = rolls[0]
        else:
            total = 0
            for roll in rolls:
                total += roll
        
        total += modifier
        return total
    
    def generate_stats(self, minus, plus):
        """Generates 6 stats and their modifiers"""
        stats = copy.deepcopy(self.base_stats)
        modifiers = {}
        for key in stats.keys():
            stats[key] = 10 + random.randint(minus, plus)
            modifer = math.floor((stats[key] - 10) / 2)
            modifiers[f'{key}_MOD'] = modifer
        
        stats_and_modifiers = {}
        stats_and_modifiers['stats'] = stats
        stats_and_modifiers['modifiers'] = modifiers
        return stats_and_modifiers
    
    def generate_hp(self, qty, sides, con_mod=0):
        """Generates hp by rolling dice and adding modifiers to the total"""
        hp = self.roll_dice(qty, sides)

        for _ in range(qty):
            hp += con_mod

        if hp <= 0:
            hp = 1
        return {'hp': hp}
    
    def generate_ac(self, base=10, dex_mod=0):
        """Generates ac by adding a modifier to a base value"""
        ac = base + dex_mod
        return {'ac': ac}
    
    def choose_weapon(self, modifiers):
        """Chooses a weapon and splits up the data into a usable form"""
        weapon = self.grabber.get_data('weapons')

        if 'Melee' in weapon['type']:
            bonus = modifiers['STR_MOD']
        else:
            bonus = modifiers['DEX_MOD']

        hit_modifier = 2 + bonus
        if hit_modifier > 0:
            hit_modifier = f'+{hit_modifier}'
        weapon['hit_modifier'] = hit_modifier
        
        if bonus != 0:
            if bonus > 0:
                bonus = f'+{bonus}'
            weapon['damage'] += f' {bonus}'

        action = {weapon.pop('weapon_name'): weapon}
        return {'actions': action}
    
    def generate_passive_perception(self, wisdom, proficiency=0):
        """Creates the passive perception for a card"""
        passive = 10 + wisdom + proficiency
        return passive
    
    def get_alignment(self):
        """Chooses an alignment based on dice rolls"""
        alignment_roll = self.roll_dice(3, 6)

        for i in self.alignments.keys():
            if alignment_roll <= i:
                alignment = random.choice(self.alignments[i])
                return alignment

    
    def data_filter_checker(self, data_filters):
        """Checks validity of provided data filters"""
        if not data_filters:
            return None
        
        DATA_FILTER_KEYS = ['race', 'gender', 'backstory']
        temp_filters = {}
        for i in data_filters.keys():
            if i in DATA_FILTER_KEYS: # Needs to be abstracted later
                temp_filters.update({i: data_filters[i]})
        data_filters = temp_filters

        if 'race' in data_filters.keys():
            try:
                if not self.grabber.get_data('races', {'race':data_filters['race']}):
                    data_filters.pop('race')
            except:
                data_filters.pop('race')

        if 'gender' in data_filters.keys():
            try:
                if not self.grabber.get_data('character_first_names', {'gender':data_filters['gender']}):
                    data_filters.pop('gender')
            except:
                data_filters.pop('gender')
        
        if 'backstory' in data_filters.keys():
            if data_filters['backstory'] == 'None':
                data_filters['backstory'] = None
        else:
            data_filters['backstory'] = None
        
        return data_filters

if __name__ == '__main__':
    creator = CardAssistant()
    # filters = {'gender':'female'}
    # print(creator.data_filter_checker({'race': 'dragon', 'gender': 'nope', 'test':'test'}))
