import os
import sys
sys.path.append(os.path.abspath(''))
from src.snap import merge_snap_data  # noqa: E402
from src import data  # noqa: E402


def check_output(actual_path, expected_path) -> None:
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_insecurity_merge() -> None:
    with_snap: data.Wrapper = merge_snap_data([('2019', 'tests/resources/SNAP_2019_test.xlsx'), ('2020', 'tests/resources/SNAP_2020_test.xlsx')])  # noqa: E501
    with open('tests/output/with_snap_actual.json', 'w+') as new_merged:  # noqa: E501
        new_merged.write(data.to_json(with_snap, pretty_print=True))
    check_output('tests/output/with_snap_actual.json', 'tests/resources/with_snap_expected.json')  # noqa: E501
