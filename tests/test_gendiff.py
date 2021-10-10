import pytest
from gendiff.scripts.gendiff import generate_diff


with open("./tests/fixtures/diff", "r") as file_diff:
    lines = file_diff.readlines()
diff_string = ''.join([line for line in lines])


def test_generate_diff_for_plain_json():
    assert generate_diff("./tests/fixtures/file1.json", "./tests/fixtures/file2.json") == diff_string

def test_generate_diff_for_plain_yaml():
    assert generate_diff("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml") == diff_string