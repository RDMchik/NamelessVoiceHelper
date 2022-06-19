import json


class JsonLoader(object):
    """is made to load json files data"""

    def load(filename: str) -> any:

        with open(filename, 'r') as file:
            data = json.load(file)

        return data

    def write(filename: str, data: any) -> None:

        with open(filename, 'w') as file:
            file.write(json.dumps(data))

    def add_change_key(filename: str, key: str, value: any) -> None:

        cur_file_data = JsonLoader.load(filename)

        cur_file_data[key] = value

        JsonLoader.write(filename, cur_file_data)