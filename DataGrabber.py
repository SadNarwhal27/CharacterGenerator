import json
import random

class DataGrabber():

    def __init__(self) -> None:
        pass

    def get_data(self, file_name:str, data_filters:dict=None):
        data_filters = self.fix_filters(data_filters)
        
        file_data = {}
        with open(f"JSONs/{file_name}.json", 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            file.close()
        
        if not data_filters:
            return file_data
        else:
            output = file_data
            print('test 1', len(output))
            for check in data_filters:
                output = {key: value for key, value in output.items() if output[key][check] == data_filters[check] or data_filters[check] in output[key][check]}
                print(output)
                print('test 2', len(output))
            return output
    
    def get_line(self, file_name:str, data_filters:dict=None):
        file_data = self.get_data(file_name, data_filters)
        pick = random.choice(list(file_data.keys()))
        return file_data[pick]
    
    def fix_filters(self, data_filters:dict):
        if data_filters:
            temp = {}
            for check in data_filters:
                if data_filters[check] != 'None':
                    temp[check] = data_filters[check]
            return temp
        else:
            return None

if __name__ == '__main__':
    grabber = DataGrabber()
    print(grabber.get_line('first_names', {'race': 'human', 'gender': 'female'}))