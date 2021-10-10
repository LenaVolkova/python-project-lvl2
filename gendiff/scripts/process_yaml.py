import yaml


def process_yaml(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)
