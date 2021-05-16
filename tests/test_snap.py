import os
import sys
import json
sys.path.append(os.path.abspath(''))
from src.snap import merge_snap_data  # noqa: E402


def check_output(actual_path, expected_path) -> None:
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_insecurity_merge() -> None:
    with open('tests/resources/df_merged_without_snap.json') as merged:
        merged_data = json.load(merged)
    with_snap = merge_snap_data([('2019', 'tests/resources/SNAP_2019_test.xlsx'), ('2020', 'tests/resources/SNAP_2020_test.xlsx')], merged_data)  # noqa: E501
    with open('tests/output/df_merged_with_snap_actual.json', 'w+') as new_merged:  # noqa: E501
        json.dump(with_snap, new_merged, separators=(',', ':'))
    check_output('tests/output/df_merged_with_snap_actual.json', 'tests/resources/df_merged_with_snap_expected.json')  # noqa: E501
