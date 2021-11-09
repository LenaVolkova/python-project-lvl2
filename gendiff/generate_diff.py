from gendiff.process_file import parse
from gendiff.formatters import stylish
from gendiff.formatters import plain
from gendiff.formatters import json_format
from gendiff.get_diff import get_diff

FORMATTER = {"json": json_format, "plain": plain, "stylish": stylish}


def generate_diff(filepath1, filepath2, format_name='stylish'):
    try:
        data1 = parse(filepath1)
        data2 = parse(filepath2)
    except ValueError as e:
        print(e)
        return
    differ = get_diff(data1, data2)
    if format_name in FORMATTER:
        return FORMATTER[format_name](differ)
    print("unknown format")
    return
