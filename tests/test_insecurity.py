import os
import sys
sys.path.append(os.path.abspath(''))
from src.insecurity import merge_ins_data  # noqa: E402


def check_output(actual_path, expected_path):
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_insecurity_merge():
    merge_ins_data('tests/resources/test_food_insecurity_merge_input.json',
                   'tests/resources/df_merged_without_insecurity.json',
                   'tests/output/df_merged_with_insecurity_actual.json')
    check_output('tests/output/df_merged_with_insecurity_actual.json',
                 'tests/resources/df_merged_with_insecurity_expected.json')


if __name__ == '__main__':
    test_insecurity_merge()