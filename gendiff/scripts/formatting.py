import json


def plain(diff):

    def correct_value(val):
        correction = {"True": "true", "False": "false", "None": "null"}
        if str(val) in correction:
            return correction[str(val)]
        if isinstance(val, int):
            return str(val)
        return "'" + str(val) + "'"

    def make_plain_strings(diff, result=[], path=[]):
        for item in diff:
            if item[0] == "both_not_equal":
                path.append(item[1])
                result = make_plain_strings(item[3], result, path)
                path.pop()
            if item[0] == "in_first":
                if item[3] == []:
                    value_from = correct_value(item[2])
                else:
                    value_from = '[complex value]'
            if item[0] == "in_second":
                if item[3] == []:
                    value_to = correct_value(item[2])
                else:
                    value_to = '[complex value]'
                path.append(item[1])
                key_path = '.'.join([str(k) for k in path])
                line = "Property '{}' was updated. From {} to {}".format(key_path, value_from, value_to)
                result.append(line)
                path.pop()
            if item[0] == "only_in_first":
                path.append(item[1])
                key_path = '.'.join([str(k) for k in path])
                line = "Property '{}' was removed".format(key_path)
                result.append(line)
                path.pop()
            if item[0] == "only_in_second":
                path.append(item[1])
                key_path = '.'.join([str(k) for k in path])
                if item[3] == []:
                    added_value = correct_value(item[2])
                else:
                    added_value = '[complex value]'
                line = "Property '{}' was added with value: {}".format(key_path, added_value)
                result.append(line)
                path.pop()
        return result

    return '\n'.join(make_plain_strings(diff))


def stylish(diff, symbol='    '):
    flags = {
        "both_equal": "    ",
        "both_not_equal": "    ",
        "in_first": "  - ",
        "in_second": "  + ",
        "only_in_first": "  - ",
        "only_in_second": "  + "}

    def correct_value(data):
        correction = {"True": "true", "False": "false", "None": "null"}
        if str(data) in correction:
            return correction[str(data)]
        return str(data)

    def formatter(diff, symbol, result='{', level=0, print_flags=True, check_level=0):
        for item in diff:
            if print_flags:
                flag = flags[str(item[0])]
            else:
                flag = "    "
            if item[3] == []:
                result += '\n{}{}{}: {}'.format(
                    symbol * level, flag, item[1], correct_value(item[2]))
            else:
                result += '\n{}{}{}: {}'.format(
                    symbol * level, flag, str(item[1]), "{")
                if (flags[item[0]] == '  - ' or flags[item[0]] == '  + ') and print_flags:
                    print_flags = False
                    check_level = level
                line = '\n' + symbol * (level + 1) + '}'
                result = formatter(
                    item[3], symbol, result, level + 1, print_flags, check_level) + line
                if level <= check_level:
                    print_flags = True
        return result
    return formatter(diff, symbol) + '\n}'


def json_format(dif):

    def make_dict(diff):
        d = {}
        for item in diff:
            if item[0] == "both_equal":
                d[item[1]] = item[2]
            if item[0] == "only_in_first":
                d[item[1]] = ["diff", item[2], None]
            if item[0] == "only_in_second":
                d[item[1]] = ["diff", None, item[2]]
            if item[0] == "both_not_equal":
                d[item[1]] = make_dict(item[3])
            if item[0] == "in_first":
                d[item[1]] = ["diff", item[2]]
            if item[0] == "in_second":
                d[item[1]].append(item[2])
        return d
    dictionary = make_dict(dif)
    result = json.dumps(dictionary, indent=4)
    return result
