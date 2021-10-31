import json
import yaml
import os


def parse(filepath):
    _, file_extension = os.path.splitext(filepath)
    if file_extension.lower() == '.json':
        return process_json(filepath)
    if file_extension.lower() == '.yaml' or file_extension.lower() == '.yml':
        return process_yaml(filepath)
    return {}


def process_json(filepath):
    with open(filepath, "r") as f:
        content = json.load(f)
    return content


def process_yaml(filepath):
    with open(filepath, "r") as f:
        content = yaml.safe_load(f)
    return content
