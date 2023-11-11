from DataGrabber import DataGrabber
import random
import copy
import math

class CardAssistant():
    def __init__(self):
        self.grabber = DataGrabber()
        self.base_stats = {"STR": 0,"DEX": 0,"CON": 0,"INT": 0,"WIS": 0,"CHA": 0}
        self.weapon_data = self.grabber.read_data_from_csv('weapons.csv')
        self.race_data = self.grabber.read_data_from_csv('races.csv')
        self.name_data = self.grabber.read_data_from_csv('character_names.csv')

    def roll_dice(self, qty, sides, modifier=0):
        """Simulates rolling dice"""
        rolls = []
        for _ in range(qty):
            roll = random.randint(1, sides)
            rolls.append(roll)
        if len(rolls) > 1:
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
        """Chooses a weapon from the weapons file"""
        weapon = self.grabber.pick_something(self.weapon_data)

        if 'Melee' in weapon['type']:
            bonus = modifiers['STR_MOD']
        else:
            bonus = modifiers['DEX_MOD']
        
        if bonus != 0:
            if bonus > 0:
                bonus = f'+{bonus}'
            weapon['damage'] += f' {bonus}'

        action = {weapon.pop('name'): weapon}
        return {'actions': action}
    
    def generate_passive_perception(self, wisdom, proficiency=0):
        passive = 10 + wisdom + proficiency
        return passive

if __name__ == '__main__':
    creator = CardAssistant()
    # filters = {'gender':'female'}
    print(creator.create_npc_card())