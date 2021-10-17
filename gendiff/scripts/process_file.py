import json
import yaml


def parse(filepath):
    if filepath[-5:] == '.json':
        return process_json(filepath)
    if filepath[-5:] == '.yaml' or filepath[-4:] == '.yml':
        return process_yaml(filepath)


def process_json(filepath):
    with open(filepath, "r") as f:
        content = json.load(f)
    return content


def process_yaml(filepath):
    with open(filepath, "r") as f:
        content = yaml.safe_load(f)
    return content
