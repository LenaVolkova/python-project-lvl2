from gendiff.common import DIFF_FLAGS


def correct_value(data):
    correction = {"True": "true", "False": "false", "None": "null"}
    if (data == True) or (data == False) or (data == None):
        return correction[str(data)]
    return str(data)


def make_strings(dif, strings, level, symbol):
    key = sorted(list(dif.keys()))
    for k in key:
        if isinstance(dif[k], dict):
            strings.append("{}{}: {}".format(symbol * (level + 1), k, "{"))
            make_strings(dif[k], strings, level + 1, symbol)
            strings.append("{}{}".format(symbol * (level + 1), "}"))
        else:
            strings.append("{}{}: {}".format(symbol * (level + 1), k, correct_value(dif[k])))


def make_stylish(diff, res=["{"], lev=0, symbol='    '):
    prefix = {str(DIFF_FLAGS[0]): "    ", str(DIFF_FLAGS[2]): "  - ", str(DIFF_FLAGS[3]): "  + "}
    keys = sorted(list(diff.keys()))
    for k in keys:
        if diff[k]["diff"] != DIFF_FLAGS[1]:
            if isinstance(diff[k]["value"], dict):
                res.append("{}{}{}: {}".format(symbol * lev, prefix[diff[k]["diff"]], k, "{"))
                make_strings(diff[k]["value"], res, lev + 1, symbol)
                res.append("{}{}".format(symbol * (lev + 1), "}"))
            else:
                res.append("{}{}{}: {}".format(
                    symbol * lev, prefix[diff[k]["diff"]], k, correct_value(diff[k]["value"])))
        else:
            if "value" not in diff[k]:
                if isinstance(diff[k]["value1"], dict):
                    res.append("{}{}{}: {}".format(symbol * lev, "  - ", k, "{"))
                    make_strings(diff[k]["value1"], res, lev + 1, symbol)
                    res.append("{}{}".format(symbol * (lev + 1), "}"))
                else:
                    res.append("{}{}{}: {}".format(symbol * lev, "  - ", k, correct_value(diff[k]["value1"])))
                if isinstance(diff[k]["value2"], dict):
                    res.append("{}{}{}: {}".format(symbol * lev, "  + ", k, "{"))
                    make_strings(diff[k]["value"], res, lev + 1, symbol)
                    res.append("{}{}".format(symbol * (lev + 1), "}"))
                else:
                    res.append("{}{}{}: {}".format(symbol * lev, "  + ", k, correct_value(diff[k]["value2"])))
            else:
                res.append("{}{}{}: {}".format(symbol * lev, "    ", k, "{"))
                make_stylish(diff[k]["value"], res, lev + 1, symbol)
                res.append("{}{}".format(symbol * (lev + 1), "}"))
    return res


def stylish(difference):
    result = []
    result = make_stylish(difference, res=["{"], lev=0, symbol='    ')
    result.append("}")
    return '\n'.join(result)
