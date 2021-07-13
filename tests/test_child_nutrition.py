
import os
import sys
sys.path.append(os.path.abspath(''))
from src.child_nutrition import merge_child_nutrition_data  # noqa: E402
from src import data  # noqa: E402


def check_output(actual_path, expected_path) -> None:
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_child_nutrition_merge() -> None:
    with_snap: data.Wrapper = merge_child_nutrition_data([('2019', 'tests/resources/child_meals_test.xlsx')])  # noqa: E501
    with open('tests/output/with_cn_actual.json', 'w+') as new_merged:  # noqa: E501
        new_merged.write(data.to_json(with_snap, pretty_print=True))
    check_output('tests/output/with_cn_actual.json', 'tests/resources/with_cn_expected.json')  # noqa: E501
