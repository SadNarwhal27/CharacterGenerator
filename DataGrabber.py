import json
import csv
import random

class DataGrabber():
    """Used to generate characters for D&D"""
    def __init__(self):
        pass

    def read_data_from_csv(self, csv_file):
        """Reads in data from a csv file"""
        csv_data = []
        with open(f'CSVs/{csv_file}', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_data.append(row)
        return csv_data

    def check_data(self, data_filters, data_to_check):
        """Checks if a row of data fits within a filter"""
        fit = False
        for i in data_filters.keys():
            if data_to_check[i] == data_filters[i]:
                fit = True
            else:
                fit = False
                return fit
        return fit

    def filter_data(self, unfiltered_data, data_filters):
        """Creates a filtered data set"""
        filtered_data = []
        for row in unfiltered_data:
            if self.check_data(data_filters, row):
                filtered_data.append(row)
        if not filtered_data:
            return None
        return filtered_data
    
    def get_row(self, gettable_data, data_filter: dict):
        """Pulls a row of data based on a filter value"""
        print(data_filter.keys())
        key_to_check = list(data_filter.keys())[0]
        for row in gettable_data:
            if row[key_to_check] == data_filter[key_to_check]:
                return row
        return None
    
    def pick_something(self, data_to_pick_from):
        """Uses the random.choice function to get a line of data"""
        pick = random.choice(data_to_pick_from)
        return pick

    def open_json(self, json_name):
        """Opens a json file and returns its data"""
        with open(json_name, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data

    def save_to_json(self, dict_data):
        """Converts a dictionary to a json file"""
        return json.dumps(dict_data, indent=4)

if __name__ == '__main__':
    gen = DataGrabber()
    filters = {'race':'human','gender':'female'}
    data = gen.filter_data(gen.read_data_from_csv('character_names.csv'), filters)
    print(gen.save_to_json(gen.pick_something(data)))
