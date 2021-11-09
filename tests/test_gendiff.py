import pytest
import json
from gendiff.generate_diff import generate_diff


testdata_stylish = [
    ("./tests/fixtures/file1.json", "./tests/fixtures/file2.json", "./tests/fixtures/simple_diff"),
    ("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml", "./tests/fixtures/simple_diff"),
    ("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath2.json", "./tests/fixtures/structured_diff"),
    ("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath2.yml", "./tests/fixtures/structured_diff"),
]

testdata_stylish_plain = [
    ("./tests/fixtures/file1.json", "./tests/fixtures/file2.json", "stylish", "./tests/fixtures/simple_diff"),
    ("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml", "stylish", "./tests/fixtures/simple_diff"),
    ("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath2.json", "stylish", "./tests/fixtures/structured_diff"),
    ("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath2.yml", "stylish", "./tests/fixtures/structured_diff"),
    ("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath2.json", 'plain', "./tests/fixtures/plain_diff"),
    ("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath2.yml", 'plain', "./tests/fixtures/plain_diff"),
]


@pytest.mark.parametrize("file1,file2,filename", testdata_stylish)
def test_generate_diff_stylish(file1, file2, filename):
    with open(filename, "r") as file_diff:
        expected = file_diff.read()
    assert generate_diff(file1, file2) == expected


@pytest.mark.parametrize("file1,file2,format,filename", testdata_stylish_plain)
def test_generate_diff_json_plain(file1, file2, format, filename):
    with open(filename, "r") as file_diff:
        expected = file_diff.read()
    assert generate_diff(file1, file2, format) == expected


def test_generate_diff_json():
    def test_json(json_string):
        try:
            json.loads(json_string)
        except ValueError:
            return False
        return True
    j_string1 = generate_diff("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath1.json", 'json')
    assert test_json(j_string1)
    j_string2 = generate_diff("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath1.yml", 'json')
    assert test_json(j_string2)
