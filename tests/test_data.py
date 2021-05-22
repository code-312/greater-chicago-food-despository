import os
import sys

# Module Not Found Error without this code
sys.path.append(os.path.abspath(''))

import pandas as pd  # noqa: E402
from src import data  # noqa: E402


def test_add():
    race_data = data.Wrapper()
    race_data.zip = {"race_total": {"60002": 24066}}
    race_data.county = {"race_total": {"17001": 66427}}
    race_data.meta.data_metrics = {"race": {"B03002_001E": "race_total"}}
    race_data.meta.data_bins = {
        "quantiles": {"race_total": [0.1, 0.2, 0.3, 0.4, 0.5]},
        "natural_breaks": {"race_total": [0.0, 0.2, 0.4, 0.6, 0.8]}}

    poverty_data = data.Wrapper()
    poverty_data.zip = {"poverty_population_total": {"60002": 24014}}
    poverty_data.county = {"poverty_population_total": {"17001": 64844}}
    poverty_data.meta.data_metrics = {"poverty": {"S1701_C01_001E": "poverty_population_total"}}  # noqa: E501
    poverty_data.meta.data_bins = {
        "quantiles": {"poverty_population_total": [0.1, 0.3, 0.5, 0.7, 0.9]},
        "natural_breaks": {"poverty_population_total": [0.6, 0.7, 0.8, 0.9, 0.11]}}  # noqa: E501

    race_data.add(poverty_data)
    assert race_data.zip["race_total"]["60002"] == 24066
    assert race_data.zip["poverty_population_total"]["60002"] == 24014
    assert race_data.county["race_total"]["17001"] == 66427
    assert race_data.county["poverty_population_total"]["17001"] == 64844
    assert race_data.meta.data_metrics["race"]["B03002_001E"] == "race_total"  # noqa: E501
    assert race_data.meta.data_metrics["poverty"]["S1701_C01_001E"] == "poverty_population_total"  # noqa: E501
    assert race_data.meta.data_bins["quantiles"]["race_total"] == [0.1, 0.2, 0.3, 0.4, 0.5]  # noqa: E501
    assert race_data.meta.data_bins["natural_breaks"]["race_total"] == [0.0, 0.2, 0.4, 0.6, 0.8]  # noqa: E501
    assert race_data.meta.data_bins["quantiles"]["poverty_population_total"] == [0.1, 0.3, 0.5, 0.7, 0.9]  # noqa: E501
    assert race_data.meta.data_bins["natural_breaks"]["poverty_population_total"] == [0.6, 0.7, 0.8, 0.9, 0.11]  # noqa: E501


def test_to_json():
    some_data = data.Wrapper()
    some_data.zip = {"race_total": {"60002": 1234}}
    some_data.county = {"race_total": {"17001": 5678}}
    some_data.meta.data_metrics = {"race": {"B03002_001E": "race_total"}}
    some_data.meta.data_bins = {
        "quantiles": {"race_total": [0.1, 0.2, 0.3, 0.4, 0.5]},
        "natural_breaks": {"race_total": [0.0, 0.2, 0.4, 0.6, 0.8]}}

    json_str = data.to_json(some_data, pretty_print=True)
    with open('./tests/resources/data_dump.json') as expected:
        assert expected.read() == json_str


def test_from_dataframe():
    df = pd.DataFrame({"fips": ["17001"], "race_total": [1234]})
    df.set_index("fips", inplace=True)
    wrapper = data.from_county_dataframe(df)
    assert wrapper.county["race_total"]["17001"] == 1234


def test_merge():
    some_data = data.Wrapper()
    some_data.meta.data_metrics = {"race": {"B03002_001E": "race_total"}}
    some_data.meta.data_bins = {"quantiles": {"race_total": [0.1, 0.2, 0.3, 0.4, 0.5]}}  # noqa: E501
    some_data.county = {
        "race_native": {
            "17001": 1234
            },
        "race_total": {
            "17001": 5678
            },
        "NAME": {
            "17001": "Adams"
            },
        "insecurity_2018": {
            "17001": {
                "total": 91011
                }
            }
        }
    some_data.zip = {"race_native": {"60002": 1357}, "race_total": {"60002": 2468}}  # noqa: E501

    merged_data = data.merge(some_data)
    assert merged_data.meta.data_metrics == some_data.meta.data_metrics
    assert merged_data.meta.data_bins == some_data.meta.data_bins
    assert merged_data.county_data["17001"]["race_data"]["race_native"] == 1234
    assert merged_data.county_data["17001"]["race_data"]["race_total"] == 5678
    assert merged_data.county_data["17001"]["insecurity_data"]["insecurity_2018"] == {"total": 91011}  # noqa: E501
    assert merged_data.county_data["17001"]["NAME"] == "Adams"
    assert merged_data.zip_data["60002"]["race_data"]["race_native"] == 1357
    assert merged_data.zip_data["60002"]["race_data"]["race_total"] == 2468


def test_calculate_natural_breaks_bins_correctly_categorizes_valid_data():
    test_zip_pct_df = {
        "poverty_population_poverty": {
            "60002": 0.075331, "60004": 0.047824, "60005": 0.079041,
            "60007": 0.038282, "60008": 0.062858, "60010": 0.042144,
            "60012": 0.024543, "60013": 0.064643, "60014": 0.066453,
            "60015": 0.044636, "60016": 0.091621, "60018": 0.138853,
            "60020": 0.087967, "60021": 0.036229, "60022": 0.024301,
            "60025": 0.061288,
        },
        "poverty_population_poverty_child": {
            "60002": 0.01978, "60004": 0.013142, "60005": 0.016204,
            "60007": 0.007048, "60008": 0.014999, "60010": 0.010662,
            "60012": 0.007078, "60013": 0.022712, "60014": 0.021133,
            "60015": 0.009923, "60016": 0.022829, "60018": 0.054427,
            "60020": 0.014337, "60021": 0.0, "60022": 0.001416,
            "60025": 0.018359,
        }
    }
    df = pd.DataFrame.from_dict(test_zip_pct_df)
    column_names = ["poverty_population_poverty",
                    "poverty_population_poverty_child"]
    actual = data.calculate_natural_breaks_bins(df,
                                                column_names,
                                                bin_count=4)

    expected = {
        'poverty_population_poverty': [
            0.024301, 0.047824, 0.066453, 0.091621, 0.138853],
        'poverty_population_poverty_child': [
            0.0, 0.007078, 0.016204, 0.022829, 0.054427]
    }

    assert actual == expected


def test_calculate_natural_breaks_removes_not_a_number_values_when_calculating_bins():  # noqa: E501
    test_zip_pct_with_nan_df = {
        "poverty_population_poverty": {
            "60002": 0.075331, "60004": None, "60005": 0.079041,
            "60007": 0.038282, "60008": 0.062858, "60010": 0.042144,
            "60012": None, "60013": 0.064643, "60014": None, "60015": 0.044636,
            "60016": 0.091621, "60018": 0.138853, "60020": 0.087967,
            "60021": 0.036229, "60022": 0.024301, "60025": None,
        },
        "poverty_population_poverty_child": {
            "60002": None, "60004": None, "60005": None, "60007": None,
            "60008": 0.014999, "60010": 0.010662, "60012": 0.007078,
            "60013": 0.022712, "60014": 0.021133, "60015": 0.009923,
            "60016": 0.022829, "60018": 0.054427, "60020": 0.014337,
            "60021": 0.0, "60022": 0.001416, "60025": 0.018359,
        }
    }
    df = pd.DataFrame.from_dict(test_zip_pct_with_nan_df)

    column_names = ["poverty_population_poverty",
                    "poverty_population_poverty_child"]
    actual = data.calculate_natural_breaks_bins(df,
                                                column_names,
                                                bin_count=2)

    expected = {
        'poverty_population_poverty': [0.024301, 0.064643, 0.138853],
        'poverty_population_poverty_child': [0.0, 0.022829, 0.054427]
    }

    assert actual == expected
