import pytest
import json
from gendiff.generate_diff import generate_diff


with open("./tests/fixtures/simple_diff", "r") as file_diff:
    lines1 = file_diff.readlines()
diff_string = ''.join([line for line in lines1])

with open("./tests/fixtures/structured_diff", "r") as file1_diff:
    lines2 = file1_diff.readlines()
structured_diff_string = ''.join([line for line in lines2])

with open("./tests/fixtures/plain_diff", "r") as file2_diff:
    lines3 = file2_diff.readlines()
plain_diff_string = ''.join([line for line in lines3])

testdata_stylish = [
    ("./tests/fixtures/file1.json", "./tests/fixtures/file2.json", diff_string),
    ("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml", diff_string),
    ("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath2.json", structured_diff_string),
    ("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath2.yml", structured_diff_string)
]

testdata_json_plain = [
    ("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath2.json", 'plain', plain_diff_string),
    ("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath2.yml", 'plain', plain_diff_string),
]


@pytest.mark.parametrize("file1,file2,expected", testdata_stylish)
def test_generate_diff_stylish(file1, file2, expected):
    assert generate_diff(file1, file2) == expected


@pytest.mark.parametrize("file1,file2,format,expected", testdata_json_plain)
def test_generate_diff_json_plain(file1, file2, format, expected):
    assert generate_diff(file1, file2, format) == expected


def test_generate_diff_json():
    def test_json(json_string):
        try:
            json.loads(json_string)
        except ValueError:
            return False
        return True
    j_string1 = generate_diff("./tests/fixtures/filepath1.json", "./tests/fixtures/filepath1.json", 'JSON')
    assert test_json(j_string1)
    j_string2 = generate_diff("./tests/fixtures/filepath1.yml", "./tests/fixtures/filepath1.yml", 'JSON')
    assert test_json(j_string2)
