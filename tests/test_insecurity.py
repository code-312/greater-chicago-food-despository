import os
import sys
sys.path.append(os.path.abspath(''))
from src.insecurity import get_food_insecurity_data  # noqa: E402
from src import data  # noqa: E402


def check_output(actual_path, expected_path):
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_insecurity_merge():

    wrapper: data.Wrapper = get_food_insecurity_data('tests/resources/insecurity')  # noqa: E501

    assert wrapper.county['insecurity_2018']['17085'] == 0.09
    assert wrapper.county['insecurity_2020_projected']['17085'] == 0.133
    assert wrapper.county['insecurity_2018_child']['17085'] == 0.128
    assert wrapper.county['insecurity_2020_child_projected']['17085'] == 0.212
    assert 'County Name' not in wrapper.county
