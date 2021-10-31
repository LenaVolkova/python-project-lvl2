#!/usr/bin/env python3


import argparse
from gendiff.generate_diff import generate_diff


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', metavar='first_file', type=str, nargs=1,
                        help='First file to compare')
    parser.add_argument('second_file', metavar='second_file', type=str, nargs=1,
                        help='Second file to compare')
    parser.add_argument('-f', '--format', help='plain or JSON')
    args = parser.parse_args()
    diff = generate_diff(args.first_file[0], args.second_file[0], args.format)
    print(diff)


if __name__ == '__main__':
    main()
