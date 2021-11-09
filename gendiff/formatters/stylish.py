from gendiff.get_diff import EQUAL, NOT_EQUAL_VALUES, ONLY_FIRST, ONLY_SECOND, NOT_EQUAL_CHILDREN

GAP = '    '
PLUS = '  + '
MINUS = '  - '
PREFIXES = {EQUAL: GAP, ONLY_FIRST: MINUS, ONLY_SECOND: PLUS}


def correct_value(data):
    if data is True:
        return "true"
    if data is False:
        return "false"
    if data is None:
        return "null"
    return str(data)


def make_strings(diff, strings, level, prefix, current_key, is_dict):
    if is_dict:
        strings.append("{}{}{}: {}".format(GAP * level, prefix, current_key, "{"))
        key = sorted(diff.keys())
        for k in key:
            make_strings(diff[k], strings, level + 1, GAP, k, isinstance(diff[k], dict))
        strings.append("{}{}".format(GAP * (level + 1), "}"))
    else:
        strings.append("{}{}{}: {}".format(GAP * level, prefix, current_key, correct_value(diff)))


def make_stylish(diff, res=["{"], lev=0):
    keys = sorted(list(diff.keys()))
    for k in keys:
        if diff[k]["diff"] not in (NOT_EQUAL_VALUES, NOT_EQUAL_CHILDREN):
            make_strings(
                diff[k]["value"], res, lev, PREFIXES[diff[k]["diff"]], k, isinstance(diff[k]["value"], dict))
        elif diff[k]["diff"] == NOT_EQUAL_VALUES:
            make_strings(diff[k]["value1"], res, lev, MINUS, k, isinstance(diff[k]["value1"], dict))
            make_strings(diff[k]["value2"], res, lev, PLUS, k, isinstance(diff[k]["value2"], dict))
        else:
            res.append("{}{}{}: {}".format(GAP * lev, GAP, k, "{"))
            make_stylish(diff[k]["value"], res, lev + 1)
            res.append("{}{}".format(GAP * (lev + 1), "}"))
    return res


def stylish(difference):
    result = make_stylish(difference, res=["{"], lev=0)
    result.append("}")
    return '\n'.join(result)
