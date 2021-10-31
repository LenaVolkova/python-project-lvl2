from gendiff.common import DIFF_FLAGS


def correct_value(data):
    correction = {"True": "true", "False": "false", "None": "null"}
    if (data == True) or (data == False) or (data == None):
        return correction[str(data)]
    return "'" + str(data) + "'"


def make_plain(dif, res, path):
    keys = sorted(list(dif.keys()))
    for k in keys:
        if dif[k]["diff"] == DIFF_FLAGS[2]:
            path.append(k)
            path_text = ".".join(path)
            res.append("Property '{}' was removed".format(path_text))
            path.pop()
        if dif[k]["diff"] == DIFF_FLAGS[3]:
            path.append(k)
            path_text = ".".join(path)
            if isinstance(dif[k]["value"], dict):
                res.append("Property '{}' was added with value: [complex value]".format(path_text))
            else:
                res.append("Property '{}' was added with value: {}".format(path_text, correct_value(dif[k]["value"])))
            path.pop()
        if dif[k]["diff"] == DIFF_FLAGS[1]:
            path.append(k)
            if "value" not in dif[k]:
                path_text = '.'.join(path)
                if isinstance(dif[k]["value1"], dict):
                    res.append("Property '{}' was updated. From [complex value] to {}".format(
                        path_text, correct_value(dif[k]["value2"])))
                elif isinstance(dif[k]["value2"], dict):
                    res.append("Property '{}' was updated. From {} to [complex value]".format(
                        path_text, correct_value(dif[k]["value1"])))
                else:
                    res.append("Property '{}' was updated. From {} to {}".format(
                        path_text, correct_value(dif[k]["value1"]), correct_value(dif[k]["value2"])))
                path.pop()
            else:
                make_plain(dif[k]["value"], res, path)
                path.pop()
    return res


def plain(diff_for_plain):
    plain_result = []
    plain_result = make_plain(diff_for_plain, [], [])
    return '\n'.join(plain_result)
