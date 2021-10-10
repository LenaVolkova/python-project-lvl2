import json


def process_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
