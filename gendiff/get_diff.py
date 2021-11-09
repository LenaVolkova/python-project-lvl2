EQUAL = "EQUAL"
NOT_EQUAL_VALUES = "NOT_EQUAL_VALUES"
ONLY_FIRST = "ONLY_FIRST"
ONLY_SECOND = "ONLY_SECOND"
NOT_EQUAL_CHILDREN = "NOT_EQUAL_CHILDREN"


def get_diff(dict1, dict2):
    diff = {}
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    common_keys = keys1 & keys2
    deleted_keys = keys1 - keys2
    added_keys = keys2 - keys1

    for k in common_keys:
        if dict1[k] == dict2[k]:
            diff[k] = {"diff": EQUAL, "value": dict1[k]}
        else:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                diff[k] = {"diff": NOT_EQUAL_CHILDREN, "value": get_diff(dict1[k], dict2[k])}
            else:
                diff[k] = {"diff": NOT_EQUAL_VALUES, "value1": dict1[k], "value2": dict2[k]}
    for k in deleted_keys:
        diff[k] = {"diff": ONLY_FIRST, "value": dict1[k]}
    for k in added_keys:
        diff[k] = {"diff": ONLY_SECOND, "value": dict2[k]}

    return diff
