import json
import pandas
from src.wic import parse_wic_pdf


def test_read_wic_data():
    participation = parse_wic_pdf(
        "tests/resources/wic_data_one_page.pdf",
        0,
        0)

    do_json_test(participation.women, "tests/output/wic_women_actual.json", "tests/resources/wic_women_expected.json")  # noqa: E501
    do_json_test(participation.infants, "tests/output/wic_infants_actual.json", "tests/resources/wic_infants_expected.json")  # noqa: E501
    do_json_test(participation.children, "tests/output/wic_children_actual.json", "tests/resources/wic_children_expected.json")  # noqa: E501
    do_json_test(participation.total, "tests/output/wic_total_actual.json", "tests/resources/wic_total_expected.json")  # noqa: E501


def do_json_test(df: pandas.DataFrame, actual_output_path: str, expected_output_path: str):  # noqa: E501
    data_dict = df.to_dict(orient="list")
    json_str = json.dumps(data_dict, indent=4, sort_keys=True)

    with open(actual_output_path, "w") as actual_output:
        actual_output.write(json_str)

    with open(expected_output_path) as expected_output_file:
        assert json_str == expected_output_file.read()
