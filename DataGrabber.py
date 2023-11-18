import json, csv, random, os
import psycopg2
from dotenv import load_dotenv

class DataGrabber():
    """Used to grab data from PostgreSQL database"""
    def __init__(self):
        load_dotenv()

        self.db_connection = psycopg2.connect(
            host=os.getenv('DB_HOSTNAME'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        self.cursor = self.db_connection.cursor()

    def get_data(self, table_name, data_filters=None) -> dict:
        query = f"SELECT * FROM {table_name}"

        if data_filters:
            query += " WHERE "
            for key in data_filters.keys():
                query += f"{key} = '{data_filters[key]}' AND "
        
            query = query[::-1].replace(' AND '[::-1], '', 1)[::-1]
        
        query += f" ORDER BY RANDOM() LIMIT 1;"
        grabbed_data = list(self.execute_command(query=query)[0])

        data_headers = self.get_data_headers(table_name=table_name)

        output_data = self.convert_to_dict(grabbed_data=grabbed_data, data_headers=data_headers)
        
        return output_data
    
    def get_data_headers(self, table_name):
        if table_name == 'races':
            output_data = ['id', 'race', 'language', 'speed', 'senses']
        else:
            query = f"SELECT COLUMN_NAME FROM INFORMATION_sCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
            headers = self.execute_command(query)
            output_data = [i[0] for i in headers]

        return output_data

    def execute_command(self, query):
        self.cursor.execute(query=query)
        executed_data = self.cursor.fetchall()
        self.db_connection.commit()
        return executed_data
    
    def convert_to_dict(self, grabbed_data:list, data_headers:list):
        grabbed_data = grabbed_data[1:]
        data_headers = data_headers[1:]

        output_data = {}
        for i in range(len(grabbed_data)):
            if type(grabbed_data[i]) == str:
                grabbed_data[i] = grabbed_data[i].rstrip()
            output_data[data_headers[i]] = grabbed_data[i]
        
        return output_data
    
    def save_to_json(self, dict_data):
        """Converts a dictionary to a json file"""
        return json.dumps(dict_data, indent=4).strip()

if __name__ == '__main__':
    gen = DataGrabber()
    test_data = gen.get_data('weapons')
    print(gen.save_to_json(test_data))

    # print(gen.get_data_headers('character_first_names'))
    
    # filters = {'race':'human','gender':'female'}
    # data = gen.filter_data(gen.read_data_from_csv('character_names.csv'), filters)
    # print(gen.save_to_json(gen.pick_something(data)))
