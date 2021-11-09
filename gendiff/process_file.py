import json
import yaml
import os


def parse(filepath):
    _, file_extension = os.path.splitext(filepath)
    file_ext = file_extension.lower()
    if file_ext == '.json':
        return process_json(filepath)
    if file_ext == '.yaml' or file_ext == '.yml':
        return process_yaml(filepath)
    raise ValueError("incorrect file type")


def process_json(filepath):
    with open(filepath, "r") as f:
        content = json.load(f)
    return content


def process_yaml(filepath):
    with open(filepath, "r") as f:
        content = yaml.safe_load(f)
    return content
