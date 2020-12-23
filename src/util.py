import json

def load_config():
    with open('../config/config.json', 'r') as config:
        return json.loads(config.read())
