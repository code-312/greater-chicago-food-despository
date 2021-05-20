import pandas as pd
from src import wic
from src import data


def test_read_wic_data():
    participation = wic.parse_wic_pdf(
        "tests/resources/wic_data_one_page.pdf",
        0,
        0)

    do_json_test(participation.women, "tests/output/wic_women_actual.json", "tests/resources/wic_women_expected.json")  # noqa: E501
    do_json_test(participation.infants, "tests/output/wic_infants_actual.json", "tests/resources/wic_infants_expected.json")  # noqa: E501
    do_json_test(participation.children, "tests/output/wic_children_actual.json", "tests/resources/wic_children_expected.json")  # noqa: E501
    do_json_test(participation.total, "tests/output/wic_total_actual.json", "tests/resources/wic_total_expected.json")  # noqa: E501


def do_json_test(df: pd.DataFrame, actual_output_path: str, expected_output_path: str):  # noqa: E501
    json_str = df.to_json(orient="index", indent=4)

    with open(actual_output_path, "w") as actual_output:
        actual_output.write(json_str)

    with open(expected_output_path) as expected_output:
        assert json_str == expected_output.read()


def test_read_csv():
    dataframe = wic.read_csv("tests/resources/wic_participation.csv")
    assert dataframe.loc["17001", "total"] == 365


def test_wrapper_from_wic_participation():

    some_data: pd.DataFrame = wic.read_csv("tests/resources/wic_participation.csv")  # noqa: E501

    participation = wic.WICParticipation(women=some_data,
                                         infants=some_data,
                                         children=some_data,
                                         total=some_data)

    wrapper: data.Wrapper = wic.wrapper_from_wic_participation(participation)

    assert wrapper.county["wic_participation_women_data"]["17001"]["race_amer_indian_or_alaskan_native"] == 3  # noqa: E501
    assert "NAME" not in wrapper.county["wic_participation_women_data"]["17001"]  # noqa: E501
    assert "natural_breaks" in wrapper.meta.data_bins
    assert "wic_participation_women_data" in wrapper.meta.data_bins["natural_breaks"]
    assert "quantiles" in wrapper.meta.data_bins
    assert "wic_participation_women_data" in wrapper.meta.data_bins["quantiles"]
