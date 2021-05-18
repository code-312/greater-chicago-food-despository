import os
import sys
sys.path.append(os.path.abspath(''))
from src.insecurity import get_food_insecurity_data  # noqa: E402
from src import data


def check_output(actual_path, expected_path):
    with open(actual_path) as actual_file:
        with open(expected_path) as expected_file:
            assert actual_file.read() == expected_file.read()


def test_insecurity_merge():

    wrapper: data.Wrapper = get_food_insecurity_data('tests/resources/insecurity')

    assert wrapper.county['2018 Child Food Insecurity  %']['17085'] == 0.128
