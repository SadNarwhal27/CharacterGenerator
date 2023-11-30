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
        self.skills = {
            'Athletics': 'STR_MOD',
            'Acrobatics': 'DEX_MOD',
            'Sleight of Hand': 'DEX_MOD',
            'Stealth': 'DEX_MOD',
            'Arcana': 'INT_MOD',
            'History': 'INT_MOD',
            'Investigation': 'INT_MOD',
            'Nature': 'INT_MOD',
            'Religion': 'INT_MOD',
            'Animal Handling': 'WIS_MOD',
            'Insight': 'WIS_MOD',
            'Medicine': 'WIS_MOD',
            'Perception': 'WIS_MOD',
            'Survival': 'WIS_MOD',
            'Deception': 'CHA_MOD',
            'Intimidation': 'CHA_MOD',
            'Performance': 'CHA_MOD',
            'Persuasion': 'CHA_MOD',
        }

    def roll_dice(self, qty:int, sides:int, modifier=0):
        """Simulates rolling dice"""
        rolls = []
        for _ in range(qty):
            roll = random.randint(1, sides)
            rolls.append(roll)
        
        # Outputs the single roll or adds the results together
        if len(rolls) == 1:
            total = rolls[0]
        else:
            total = 0
            for roll in rolls:
                total += roll
        
        total += modifier
        return total
    
    def generate_stats(self, minus:int, plus:int):
        """Generates 6 stats and their modifiers"""

        # So the initial copy is not tampered with
        stats = copy.deepcopy(self.base_stats)

        # Calculates associated stats and modifiers
        modifiers = {}
        for key in stats.keys():
            stats[key] = 10 + random.randint(minus, plus)
            modifer = math.floor((stats[key] - 10) / 2)
            modifiers[f'{key}_MOD'] = modifer
        
        stats_and_modifiers = {}
        stats_and_modifiers['stats'] = stats
        stats_and_modifiers['modifiers'] = modifiers
        return stats_and_modifiers
    
    def generate_hp(self, qty:int, sides:int, con_mod=0):
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
    
    def choose_weapon(self, modifiers:dict):
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
    
    def generate_passive_perception(self, wisdom:int, proficiency=0):
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

    def generate_skills(self, raw_skills:str, modifiers:dict):
        """Generates usable skills for the character"""
        individual_skills = [i.lstrip() for i in raw_skills.split(',')]

        modified_skills = ""
        for skill in individual_skills:
            mod = modifiers[self.skills[skill]] + 2
            if mod > 0:
                modified_skills += "+"

            modified_skills += f"{mod} {skill}, "
        
        # The string slice removes the trailing ', ' from the modified_skills
        return modified_skills[:-2]
    
    def data_filter_checker(self, data_filters:dict):
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
    mods = { "STR_MOD": -1, "DEX_MOD": -1, "CON_MOD": -1, "INT_MOD": -1, "WIS_MOD": -1, "CHA_MOD": 0 }
    print(creator.generate_skills("Perception, Deception, Sleight of Hand", mods))