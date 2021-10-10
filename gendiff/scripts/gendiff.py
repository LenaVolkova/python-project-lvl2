#!/usr/bin/env python


import sys
import argparse
import yaml
from gendiff.scripts.process_json import process_json 
from gendiff.scripts.process_yaml import process_yaml
from operator import itemgetter



def generate_diff(filepath1, filepath2):
    data1 = {}
    data2 = {}
    data_diff = []
    result_diff = ""

    if filepath1[-5:] == '.json':
        content1 = process_json(filepath1)
        content2 = process_json(filepath2)

    if filepath1[-5:] == '.yaml' or filepath1[-4:] == '.yml':
        content1 = process_yaml(filepath1)
        content2 = process_yaml(filepath2)
        
    for key1, value1 in content1.items():
        if str(value1) == "True":
            value1 = "true"
        if str(value1) == "False":
            value1 = "false"
        data1[key1] = value1
    for key2, value2 in content2.items():
        if str(value2) == "True":
            value2 = "true"
        if str(value2) == "False":
            value2 = "false"
        data2[key2] = value2
    

    for key in data1:
        if key in data2 and data1[key] == data2[key]:
            data_diff.append((' ', key, data1[key]))
        elif key in data2 and data1[key] != data2[key]:
            data_diff.append(('-', key, data1[key]))
            data_diff.append(('+', key, data2[key]))
        else:
            data_diff.append(('-', key, data1[key]))
    for key in data2:
        if key not in data1:
            data_diff.append(('+', key, data2[key]))

    data_diff.sort(key=itemgetter(1))

    result_diff = "{\n"
    for item in data_diff:
        result_diff += '  {} {}: {}\n'.format(str(item[0]), str(item[1]), str(item[2]))
    result_diff += "}"
    return result_diff


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
    print(diff)


if __name__ == '__main__':
    main()
