
import os
import sys
sys.path.append(os.path.abspath(''))
from src.file_to_json import file_to_json  # noqa: E402


def check_output(actual_path, expected_path):
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def clean_output(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def test_file_to_json():
    try:
        file_to_json('tests/resources', 'tests/resources', blacklist=['Key'])
        check_output('tests/resources/Countytest_food_insecurity_xls.json',
                     'tests/resources/test_food_insecurity_expected.json')
        check_output('tests/resources/Countytest_food_insecurity_xlsx.json',
                     'tests/resources/test_food_insecurity_expected.json')
        check_output('tests/resources/test_food_insecurity_csv.json',
                     'tests/resources/test_food_insecurity_expected.json')
    finally:
        clean_output('tests/resources/Countytest_food_insecurity_xls.json')
        clean_output('tests/resources/Countytest_food_insecurity_xlsx.json')
        clean_output('tests/resources/test_food_insecurity_csv.json')


if __name__ == '__main__':
    test_file_to_json()
