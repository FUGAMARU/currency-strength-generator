import os
import json


def get_config():
    with open(f"{os.getcwd()}/config.json") as file:
        return json.load(file)
