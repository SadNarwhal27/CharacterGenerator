import os, json

def get_spell_data(path, limit=999):
    spell_list = os.listdir(path)
    rounds = 0 

    spells = []
    for spell in spell_list:

        rounds += 1
        temp = ''
        with open(f"{path}\\{spell}", 'r', encoding='utf-8') as marked_spell:
            temp = marked_spell.readlines()
            marked_spell.close()

        important_bits = []
        things_to_look_for = ['title:', 'tags:', '**Casting Time**', '**Range**', '**Components**', '**Duration**', 'At Higher Levels.', 'subtags']
        
        description_start = False
        description = '**Description** '

        creature_start = False
        creature = '**Creature** '

        for line in temp:
            if 'At Higher Levels.' in line:
                description_start = False
                important_bits.append(description.strip())
                important_bits.append(line.strip())
                continue

            if '## ' in line:
                creature_start = True
                description_start = False
            
            if description_start:
                description += line
                continue

            if creature_start:
                creature += line
                continue

            for thing in things_to_look_for:
                if thing in line:
                    important_bits.append(line.strip())
                    continue
            
            if '**Duration**' in line:
                description_start = True
        
        if 'Description' not in important_bits:
            important_bits.append(description.strip())

        if creature.strip() != '**Creature**':
            important_bits.append(creature.strip())
        
        output = list(dict.fromkeys(important_bits))

        spells.append(output)

        if rounds >= limit:
            return spells
    
    return spells

def write_txt_file(output:list, file_name:str, destination_path):
    with open(f"{destination_path}\\{file_name}.txt", 'w', encoding='utf-8') as file:
        for line in output:
            file.write(line + '\n')
        file.close()

def get_tags(raw_tags:str, sub=False):
    tag_list = raw_tags.replace('[', '').replace(']', '').replace(',', '').split()
    schools = ['abjuration', 'conjuration', 'divination', 'enchantment', 'evocation', 'illusion', 'necromancy', 'transmutation']
    classes = ['artificer', 'bard', 'cleric', 'druid', 'paladin', 'ranger', 'sorcerer', 'warlock', 'wizard']

    spell_classes = []
    tag_dict = {}
    for tag in tag_list:
        if tag == 'cantrip':
            tag_dict['spell_level'] = 'Cantrip'
            continue
        elif 'level' in tag:
            tag_dict['spell_level'] = tag.replace('level', '')
            continue
        elif tag in schools:
            tag_dict['spell_school'] = tag.capitalize()
        elif tag in classes:
            spell_classes.append(tag)
    tag_dict['spell_classes'] = spell_classes
    return tag_dict


def list_to_dict(spells):
    output = {}
    for line in spells:

        title = line[0].replace('title: ', '').replace('"', '').strip()

        if '**Creature**' in line:
            write_txt_file(line, title)
            continue

        output[title] = {'spell_name': title}

        for part in line:
            if 'tags: ' in part and 'subtags' not in part:
                temp = part.replace('tags: ', '')
                output[title].update(get_tags(temp))
                continue
            elif 'subtags: ' in part:
                temp = part.replace('subtags: ', '').replace('[', '').replace(']', '').split(',')

                subclasses = {}
                for subclass in temp:
                    subclass = subclass.split(':')
                    subclasses[subclass[0].strip()] = subclass[1].strip()
                output[title]['spell_subclasses'] = subclasses
                continue
            elif '**Casting Time**: ' in part:
                temp = part.replace('**Casting Time**: ', '')
                output[title]['spell_cast_time'] = temp
                continue
            elif '**Range**: ' in part:
                temp = part.replace('**Range**: ', '')
                output[title]['spell_range'] = temp
                continue
            elif '**Components**: ' in part:
                temp = part.replace('**Components**: ', '')
                output[title]['spell_components'] = temp
                continue
            elif '**Duration**: ' in part:
                temp = part.replace('**Duration**: ', '')
                output[title]['spell_duration'] = temp
                continue
            elif '**Description** ' in part:
                temp = part.replace('**Description** ', '')
                output[title]['spell_description'] = temp.strip()
                continue
            elif 'At Higher Levels.' in part:
                temp = part.replace('At Higher Levels.', '').replace('*', '')
                output[title]['spell_higher_level'] = temp.strip()
                continue
            elif '**Creature** ' in part:
                temp = part.replace('**Creature** ', '')
                output[title]['spell_creature'] = temp.strip()
                continue

        if 'spell_higher_level' not in output[title].keys():
            output[title]['spell_higher_level'] = None
        
        if 'spell_subclasses' not in output[title].keys():
            temp = {}
            for key in output[title]:
                temp[key] = output[title][key]

                if key == "spell_classes":
                    temp.update({"spell_subclasses": None})
            output[title] = temp

    return output

def create_json(spells:dict):

    with open('spells.json', 'w', encoding='utf-8') as file:
        json.dump(spells, file, indent=4)

spells = get_spell_data()
create_json(list_to_dict(spells))