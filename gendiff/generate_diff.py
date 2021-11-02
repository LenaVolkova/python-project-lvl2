from gendiff.process_file import parse
from gendiff.stylish import stylish
from gendiff.plain import plain
from gendiff.json_form import json_format
from gendiff.common import DIFF_FLAGS

FORMATTER = {"json": json_format, "plain": plain, "stylish": stylish}


def generate_diff(filepath1, filepath2, format_name=''):
    data1 = {}
    data2 = {}
    data1 = parse(filepath1)
    data2 = parse(filepath2)
    differ = {}
    differ = get_diff(data1, data2)
    if format_name in FORMATTER:
        return FORMATTER[format_name](differ)
    return stylish(differ)


def get_diff(dict1, dict2):
    diff = {}
    if isinstance(dict1, dict):
        keys1 = dict1.keys()
    if isinstance(dict2, dict):
        keys2 = dict2.keys()
    common_keys = keys1 & keys2
    deleted_keys = keys1 - keys2
    added_keys = keys2 - keys1

    for k in common_keys:
        if dict1[k] == dict2[k]:
            diff[k] = {"diff": DIFF_FLAGS[0], "value": dict1[k]}
        else:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                diff[k] = {"diff": DIFF_FLAGS[1], "value": get_diff(dict1[k], dict2[k])}
            else:
                diff[k] = {"diff": DIFF_FLAGS[1], "value1": dict1[k], "value2": dict2[k]}
    for k in deleted_keys:
        diff[k] = {"diff": DIFF_FLAGS[2], "value": dict1[k]}
    for k in added_keys:
        diff[k] = {"diff": DIFF_FLAGS[3], "value": dict2[k]}

    return diff
