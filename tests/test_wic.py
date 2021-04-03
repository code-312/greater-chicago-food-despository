from src.wic import parse_wic_pdf


def test_read_wic_data():
    parse_wic_pdf(
        "tests/resources/wic_data_one_page.pdf",
        "tests/resources/test_wic_actual_output.csv",
        0,
        0)

    with open("tests/resources/test_wic_actual_output.csv") \
            as actual_output_file:

        actual_output_text = actual_output_file.read()

        with open("tests/resources/test_wic_expected_output.txt") \
                as expected_output_file:

            expected_output_text = expected_output_file.read()

            assert actual_output_text == expected_output_text
