import os
import sys
sys.path.append(os.path.abspath(''))
from src.insecurity import get_food_insecurity_data  # noqa: E402
from src import data  # noqa: E402


def test_get_food_insecurity_data():

    wrapper: data.Wrapper = get_food_insecurity_data('tests/resources/insecurity')  # noqa: E501

    assert wrapper.county['insecurity_2018']['17085'] == 0.09
    assert wrapper.county['insecurity_2020_projected']['17085'] == 0.133
    assert wrapper.county['insecurity_2018_child']['17085'] == 0.128
    assert wrapper.county['insecurity_2020_child_projected']['17085'] == 0.212
    assert 'County Name' not in wrapper.county
    assert wrapper.meta.data_bins['natural_breaks']['insecurity_2018'] == [0.048, 0.071, 0.09, 0.116, 0.119]
    assert wrapper.meta.data_bins['natural_breaks']['insecurity_2020_projected'] == [0.092, 0.116, 0.133, 0.157, 0.163]
    assert wrapper.meta.data_bins['natural_breaks']['insecurity_2018_child'] == [0.064, 0.094, 0.128, 0.157, 0.182]
    assert wrapper.meta.data_bins['natural_breaks']['insecurity_2020_child_projected'] == [0.15, 0.183, 0.212, 0.238, 0.268]
    assert wrapper.meta.data_bins['quantiles']['insecurity_2018'] == [0.048, 0.071, 0.09, 0.116, 0.119]
    assert wrapper.meta.data_bins['quantiles']['insecurity_2020_projected'] == [0.092, 0.116, 0.133, 0.157, 0.163]
    assert wrapper.meta.data_bins['quantiles']['insecurity_2018_child'] == [0.064, 0.094, 0.128, 0.157, 0.182]
    assert wrapper.meta.data_bins['quantiles']['insecurity_2020_child_projected'] == [0.15, 0.183, 0.212, 0.238, 0.268]
