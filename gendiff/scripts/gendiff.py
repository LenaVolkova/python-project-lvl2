#!/usr/bin/env python


import sys
import argparse
from gendiff.scripts.process_json import process_json
from gendiff.scripts.process_yaml import process_yaml


def generate_diff(filepath1, filepath2):
    data1 = {}
    data2 = {}

    if filepath1[-5:] == '.json':
        data1 = process_json(filepath1)
        data2 = process_json(filepath2)
    if filepath1[-5:] == '.yaml' or filepath1[-4:] == '.yml':
        data1 = process_yaml(filepath1)
        data2 = process_yaml(filepath2)

    diff = get_diff(data1, data2)

    return diff


def get_diff(dict1, dict2):
    diff = []
    keys1 = set()
    keys2 = set()
    if isinstance(dict1, dict):
        keys1 = {k for k in dict1}
    if isinstance(dict2, dict):
        keys2 = {k for k in dict2}
    keys = sorted(list(keys1 | keys2))

    if keys == []:
        return diff

    for k in keys:
        if k in dict1 and k in dict2:
            if dict1[k] == dict2[k]:
                diff.append(('0', k, dict1[k], get_diff(dict1[k], dict2[k])))
            else:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    diff.append(('0', k, dict1[k], get_diff(dict1[k], dict2[k])))
                else:
                    if not isinstance(dict1[k], dict):
                        diff.append(('1', k, dict1[k], []))
                        diff.append(('2', k, dict2[k], get_diff({}, dict2[k])))
                    elif not isinstance(dict2[k], dict):
                        diff.append(('1', k, dict1[k], get_diff(dict1[k], {})))
                        diff.append(('2', k, dict2[k], []))
        if k in dict1 and k not in dict2:
            diff.append(('1', k, dict1[k], get_diff(dict1[k], {})))
        if k not in dict1 and k in dict2:
            diff.append(('2', k, dict2[k], get_diff({}, dict2[k])))

    return diff


def stylish(diff, symbol='    '):
    flags = {"0": "    ", "1": "  - ", "2": "  + "}

    def formatter(diff, symbol, result='{', level=0, print_flags=True, check_level=0):
        for item in diff:
            if print_flags:
                flag = flags[str(item[0])]
            else:
                flag = flags["0"]
            if item[3] == []:
                result += '\n{}{}{}: {}'.format(
                    symbol * level, flag, str(item[1]), str(item[2]))
            else:
                result += '\n{}{}{}: {}'.format(
                    symbol * level, flag, str(item[1]), "{")
                if (str(item[0]) == '1' or str(item[0]) == '2') and print_flags:
                    print_flags = False
                    check_level = level
                line = '\n' + symbol * (level + 1) + '}'
                result = formatter(
                    item[3], symbol, result, level + 1, print_flags, check_level) + line
                if level <= check_level:
                    print_flags = True
        return result
    return formatter(diff, symbol) + '\n}'


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
#
# args = parser.parse_args()
# print(args.accumulate(args.integers))
    parser.add_argument('first_file', metavar='first_file', type=str, nargs=1,
                        help='First file to compare')
    parser.add_argument('second_file', metavar='second_file', type=str, nargs=1,
                        help='Second file to compare')
    parser.add_argument('-f', '--format', help='plain or JSON')
    args = parser.parse_args()
    print(args)
    diff = generate_diff(sys.argv[1], sys.argv[2])
    print(stylish(diff))


if __name__ == '__main__':
    main()
