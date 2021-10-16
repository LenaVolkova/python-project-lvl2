import json


def process_json(filepath):
    with open(filepath, "r") as f:
        content = json.load(f)

        def correct_dict(content):
            data = {}
            correction = {"True": "true", "False": "false", "None": "null"}
            for key, value in content.items():
                if str(value) in correction:
                    value = correction[str(value)]
                data[key] = value
                if isinstance(value, dict):
                    data[key] = correct_dict(value)
            return data
    return correct_dict(content)
