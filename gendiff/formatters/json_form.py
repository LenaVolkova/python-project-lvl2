import json
from gendiff.get_diff import EQUAL, NOT_EQUAL_CHILDREN, NOT_EQUAL_VALUES, ONLY_FIRST, ONLY_SECOND


def make_dict(diff):
    new_dict = {}
    for k in diff:
        if diff[k]["diff"] == EQUAL:
            new_dict[k] = diff[k]["value"]
        if diff[k]["diff"] == NOT_EQUAL_CHILDREN:
            new_dict[k] = make_dict(diff[k]["value"])
        if diff[k]["diff"] == NOT_EQUAL_VALUES:
            new_dict[k] = (NOT_EQUAL_VALUES, diff[k]["value1"], diff[k]["value2"])
        if diff[k]["diff"] == ONLY_FIRST:
            new_dict[k] = (ONLY_FIRST, diff[k]["value"])
        if diff[k]["diff"] == ONLY_SECOND:
            new_dict[k] = (ONLY_SECOND, diff[k]["value"])
    return new_dict


def json_format(difference):
    dictionary = make_dict(difference)
    result = []
    result = json.dumps(dictionary, indent=4)
    return result
