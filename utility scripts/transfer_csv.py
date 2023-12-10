import os, json, csv

def read_csv(path:str, file_name:str):
    lines = {}
    with open(f'{path}\\{file_name + '.csv'}', 'r', encoding='utf-8') as f:
        csv_file = csv.reader(f)
        for line in csv_file:
            lines[line[1].strip()] = [part.strip() for part in line[1:]]
    return lines

def create_json(csv_data:dict, new_file_name:str, columns:list):
    new_file = {}
    for line in csv_data:
        temp = {}
        for column in range(len(columns)):
            temp[columns[column]] = csv_data[line][column]
        new_file[line] = temp
    
    with open(new_file_name + '.json', 'w', encoding='utf-8') as f:
        json.dump(new_file, f, indent=4)

if __name__ == '__main__':
    create_json(read_csv("C:\\Users\\schal\\Downloads\\Export DB Files", "character_first_names"), 'first_names', ['first_name', 'race', 'gender'])