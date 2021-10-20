from gendiff.scripts.gendiff import generate_diff


with open("./tests/fixtures/simple_diff", "r") as file_diff:
    lines = file_diff.readlines()
diff_string = ''.join([line for line in lines])

with open("./tests/fixtures/structured_diff", "r") as file1_diff:
    lines = file1_diff.readlines()
structured_diff_string = ''.join([line for line in lines])

with open("./tests/fixtures/plain_diff", "r") as file2_diff:
    lines = file2_diff.readlines()
plain_diff_string = ''.join([line for line in lines])

with open("./tests/fixtures/diff.json", "r") as file3_diff:
    lines = file3_diff.readlines()
json_diff_string = ''.join([line for line in lines])


def test_generate_diff_for_simple_json():
    assert generate_diff("./tests/fixtures/file1.json", "./tests/fixtures/file2.json") == diff_string


def test_generate_diff_for_simple_yaml():
    assert generate_diff("./tests/fixtures/file1.yaml", "./tests/fixtures/file2.yaml") == diff_string


def test_generate_diff_for_json():
    filepath1 = "./tests/fixtures/filepath1.json"
    filepath2 = "./tests/fixtures/filepath2.json"
    assert generate_diff(filepath1, filepath2) == structured_diff_string


def test_generate_diff_for_yaml():
    filepath1 = "./tests/fixtures/filepath1.yml"
    filepath2 = "./tests/fixtures/filepath2.yml"
    assert generate_diff(filepath1, filepath2) == structured_diff_string


def test_generate_plain_diff_for_json():
    filepath1 = "./tests/fixtures/filepath1.json"
    filepath2 = "./tests/fixtures/filepath2.json"
    assert generate_diff(filepath1, filepath2, 'plain') == plain_diff_string


def test_generate_plain_diff_for_yaml():
    filepath1 = "./tests/fixtures/filepath1.yml"
    filepath2 = "./tests/fixtures/filepath2.yml"
    assert generate_diff(filepath1, filepath2, 'plain') == plain_diff_string


def test_generate_json_diff_for_json():
    filepath1 = "./tests/fixtures/filepath1.json"
    filepath2 = "./tests/fixtures/filepath2.json"
    assert generate_diff(filepath1, filepath2, 'JSON') == json_diff_string


def test_generate_json_diff_for_yaml():
    filepath1 = "./tests/fixtures/filepath1.yml"
    filepath2 = "./tests/fixtures/filepath2.yml"
    assert generate_diff(filepath1, filepath2, 'JSON') == json_diff_string