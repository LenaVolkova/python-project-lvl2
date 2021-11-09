from gendiff.get_diff import EQUAL, NOT_EQUAL_VALUES, ONLY_FIRST, ONLY_SECOND, NOT_EQUAL_CHILDREN

PREFIXES = {EQUAL: "    ", ONLY_FIRST: "  - ", ONLY_SECOND: "  + "}


def correct_value(data):
    if data is True:
        return "true"
    if data is False:
        return "false"
    if data is None:
        return "null"
    return str(data)


def make_strings(diff, strings, level, symbol, prefix, current_key, is_dict):
    if is_dict:
        strings.append("{}{}{}: {}".format(symbol * level, prefix, current_key, "{"))
        key = sorted(diff.keys())
        for k in key:
            make_strings(diff[k], strings, level + 1, symbol, '    ', k, isinstance(diff[k], dict))
        strings.append("{}{}".format(symbol * (level + 1), "}"))
    else:
        strings.append("{}{}{}: {}".format(symbol * level, prefix, current_key, correct_value(diff)))


def make_stylish(diff, res=["{"], lev=0, symbol='    '):
    keys = sorted(list(diff.keys()))
    for k in keys:
        if diff[k]["diff"] not in (NOT_EQUAL_VALUES, NOT_EQUAL_CHILDREN):
            make_strings(
                diff[k]["value"], res, lev, symbol, PREFIXES[diff[k]["diff"]], k, isinstance(diff[k]["value"], dict))
        elif diff[k]["diff"] == NOT_EQUAL_VALUES:
            make_strings(diff[k]["value1"], res, lev, symbol, "  - ", k, isinstance(diff[k]["value1"], dict))
            make_strings(diff[k]["value2"], res, lev, symbol, "  + ", k, isinstance(diff[k]["value2"], dict))
        else:
            res.append("{}{}{}: {}".format(symbol * lev, "    ", k, "{"))
            make_stylish(diff[k]["value"], res, lev + 1, symbol)
            res.append("{}{}".format(symbol * (lev + 1), "}"))
    return res


def stylish(difference):
    result = make_stylish(difference, res=["{"], lev=0, symbol='    ')
    result.append("}")
    return '\n'.join(result)
