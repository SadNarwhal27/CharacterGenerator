import json, os
import psycopg2
from dotenv import load_dotenv

class DataGrabber():
    """Used to grab data from PostgreSQL database"""
    def __init__(self):
        load_dotenv()

        self.db_connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
        self.cursor = self.db_connection.cursor()

    def get_data(self, table_name:str, data_filters:dict=None) -> dict:
        """Gets data from a database table with or without filters by building a SQL query"""

        query = f"SELECT * FROM {table_name}"

        if data_filters:
            query += " WHERE "
            for key in data_filters.keys():
                query += f"{key} = '{data_filters[key]}' AND "

            # Might be able to simplify to a string slice like [:-5]
            query = query[::-1].replace(' AND '[::-1], '', 1)[::-1]
        
        # How we get a random row from the table
        query += f" ORDER BY RANDOM() LIMIT 1;"
        grabbed_data = list(self.execute_command(query=query)[0])

        data_headers = self.get_data_headers(table_name=table_name)

        output_data = self.convert_to_dict(grabbed_data=grabbed_data, data_headers=data_headers)
        
        return output_data
    
    def get_data_headers(self, table_name:str):
        """Gets the database table headers to user later"""

        # Ran into an alphabetical issue with this so needed an exception
        if table_name == 'races':
            output_data = ['id', 'race', 'language', 'speed', 'senses']
        else:
            query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';"
            headers = self.execute_command(query)
            output_data = [i[0] for i in headers]

        return output_data

    def execute_command(self, query:str):
        """Puts the database query we made into action"""

        self.cursor.execute(query=query)
        executed_data = self.cursor.fetchall()
        self.db_connection.commit()
        return executed_data
    
    def convert_to_dict(self, grabbed_data:list, data_headers:list):
        """Combines two sepperate lists into a dict"""

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
