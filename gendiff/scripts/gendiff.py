#!/usr/bin/env python3


import argparse
from gendiff.scripts.process_file import parse
from gendiff.scripts.formatting import plain, stylish, json_format


def generate_diff(filepath1, filepath2, format_name=''):
    data1 = {}
    data2 = {}
    data1 = parse(filepath1)
    data2 = parse(filepath2)
    diff = get_diff(data1, data2)
    if format_name == 'JSON':
        return json_format(diff)
    if format_name == 'plain':
        return plain(diff)
    return stylish(diff)


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
                diff.append(('both_equal', k, dict1[k], get_diff(dict1[k], dict2[k])))
            else:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    diff.append(('both_not_equal', k, dict1[k], get_diff(dict1[k], dict2[k])))
                else:
                    if not isinstance(dict1[k], dict):
                        diff.append(('in_first', k, dict1[k], []))
                        diff.append(('in_second', k, dict2[k], get_diff({}, dict2[k])))
                    elif not isinstance(dict2[k], dict):
                        diff.append(('in_first', k, dict1[k], get_diff(dict1[k], {})))
                        diff.append(('in_second', k, dict2[k], []))
        if k in dict1 and k not in dict2:
            diff.append(('only_in_first', k, dict1[k], get_diff(dict1[k], {})))
        if k not in dict1 and k in dict2:
            diff.append(('only_in_second', k, dict2[k], get_diff({}, dict2[k])))

    return diff


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
    diff = generate_diff(args.first_file[0], args.second_file[0], args.format)
    print(diff)


if __name__ == '__main__':
    main()
