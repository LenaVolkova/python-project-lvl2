import pytest
from gendiff.scripts.gendiff import generate_diff, stylish


with open("./tests/fixtures/diff", "r") as file_diff:
    lines = file_diff.readlines()
diff_string = ''.join([line for line in lines])

with open("./tests/fixtures/nested_diff", "r") as file1_diff:
    lines = file1_diff.readlines()
nested_diff_string = ''.join([line for line in lines])


def test_generate_diff_for_plain_json():
    assert stylish(generate_diff("./tests/fixtures/file1.json", "./tests/fixtures/file2.json")) == diff_string


def test_generate_diff_for_plain_yaml():
    assert stylish(generate_diff("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml")) == diff_string


def test_generate_diff_for_nested_json():
    filepath1 = "./tests/fixtures/filepath1.json"
    filepath2 = "./tests/fixtures/filepath2.json"
    assert stylish(generate_diff(filepath1, filepath2), '    ') == nested_diff_string

def test_generate_diff_for_nested_yaml():
    filepath1 = "./tests/fixtures/filepath1.yml"
    filepath2 = "./tests/fixtures/filepath2.yml"
    assert stylish(generate_diff(filepath1, filepath2), '    ') == nested_diff_string
