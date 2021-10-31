import json
from gendiff.common import DIFF_FLAGS


def make_dict(diff):
    new_dict = {}
    for k in diff:
        if diff[k]["diff"] == DIFF_FLAGS[0]:
            new_dict[k] = diff[k]["value"]
        if diff[k]["diff"] == DIFF_FLAGS[1]:
            if "value" in diff[k]:
                new_dict[k] = make_dict(diff[k]["value"])
            else:
                new_dict[k] = (DIFF_FLAGS[1], diff[k]["value1"], diff[k]["value2"])
        if diff[k]["diff"] == DIFF_FLAGS[2]:
            new_dict[k] = (DIFF_FLAGS[2], diff[k]["value"])
        if diff[k]["diff"] == DIFF_FLAGS[3]:
            new_dict[k] = (DIFF_FLAGS[3], diff[k]["value"])
    return new_dict


def json_format(difference):
    dictionary = make_dict(difference)
    result = []
    result = json.dumps(dictionary, indent=4)
    return result
