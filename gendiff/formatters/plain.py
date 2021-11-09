from gendiff.formatters.stylish import make_strings
from gendiff.get_diff import EQUAL, NOT_EQUAL_VALUES, ONLY_FIRST, ONLY_SECOND, NOT_EQUAL_CHILDREN


def correct_value(data):
    if data is True:
        return "true"
    if data is False:
        return "false"
    if data is None:
        return "null"
    if isinstance(data, dict):
        return "[complex value]"
    if isinstance(data, int) or isinstance(data, float):
        return str(data)
    return "'" + str(data) + "'"


def make_string(res, path_text, diff_k):
    if diff_k["diff"] == ONLY_FIRST:
        res.append("Property '{}' was removed".format(path_text))
    if diff_k["diff"] == ONLY_SECOND:
        res.append("Property '{}' was added with value: {}".format(path_text, correct_value(diff_k["value"])))
    if diff_k["diff"] == NOT_EQUAL_VALUES:
        res.append("Property '{}' was updated. From {} to {}".format(
            path_text, correct_value(diff_k["value1"]), correct_value(diff_k["value2"])))


def make_plain(diff, result, path):
    keys = sorted(diff.keys())
    for k in keys:
        if diff[k]["diff"] != EQUAL:
            path.append(k)
            path_txt = ".".join(path)
            if diff[k]["diff"] != NOT_EQUAL_CHILDREN:
                path.pop()
        make_string(result, path_txt, diff[k])
        if diff[k]["diff"] == NOT_EQUAL_CHILDREN:
            make_plain(diff[k]["value"], result, path)
            path.pop()
    return result


def plain(diff_for_plain):
    plain_result = []
    plain_result = make_plain(diff_for_plain, [], [])
    return '\n'.join(plain_result)
