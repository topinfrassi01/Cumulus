import json
import os


class Configuration:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../config.json')

        with open(filename) as json_data:
            self._config = json.load(json_data)

    def __getitem__(self, key):
        return self._config[key]
