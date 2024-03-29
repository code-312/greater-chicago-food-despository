import os
import re
import pdfplumber
import pandas as pd
from typing import List, Dict
from src import data


'''
GCFD staff provided a pdf illinois_wic_data_january_2021.pdf which contains WIC
data for 96 out of 102 IL Counties. We do not know why some counties are
missing. Data is for the month of January year 2021. wic.py reads thru each
line of each page of the pdf looking for lines that contain the data we want
and then saves that data to a dataframe. GCFD staff also requested a .csv
version of the data'''


def is_up_to_date(input_file_path: str, output_file_path: str) -> bool:
    try:
        return os.path.getmtime(output_file_path) > \
            os.path.getmtime(input_file_path)
    except FileNotFoundError:
        return False


class WICParticipation:
    def __init__(self,
                 women: pd.DataFrame,
                 infants: pd.DataFrame,
                 children: pd.DataFrame,
                 total: pd.DataFrame):
        self.women = women
        self.infants = infants
        self.children = children
        self.total = total


def read_wic_data(always_run: bool = False) -> data.Wrapper:

    input_file_path = "data_folder/illinois_wic_data_january_2021.pdf"
    women_output_csv_path = "final_jsons/wic_participation_women.csv"
    infants_output_csv_path = "final_jsons/wic_participation_infants.csv"
    children_output_csv_path = "final_jsons/wic_participation_children.csv"
    total_output_csv_path = "final_jsons/wic_participation_total.csv"

    if always_run or \
       not is_up_to_date(input_file_path, women_output_csv_path) or \
       not is_up_to_date(input_file_path, infants_output_csv_path) or \
       not is_up_to_date(input_file_path, children_output_csv_path) or \
       not is_up_to_date(input_file_path, total_output_csv_path):
        # PDF has 97 pages. Skip page 0 because it shows Statewide totals
        # which we don't need
        participation: WICParticipation = parse_wic_pdf(
            input_file_path,
            1,
            96)

        participation.women.to_csv(women_output_csv_path)
        participation.children.to_csv(children_output_csv_path)
        participation.infants.to_csv(infants_output_csv_path)
        participation.total.to_csv(total_output_csv_path)

        return wrapper_from_wic_participation(participation)
    else:
        participation = WICParticipation(
            women=read_csv(women_output_csv_path),
            infants=read_csv(infants_output_csv_path),
            children=read_csv(children_output_csv_path),
            total=read_csv(total_output_csv_path))

        return wrapper_from_wic_participation(participation)


def read_csv(path: str) -> pd.DataFrame:
    # Using index_col="fips" in the read_csv() call made the fips column int
    # datatype for some reason, so we set the index on a separate line
    df = pd.read_csv(path, dtype={"fips": str})
    return df.set_index("fips")


def read_json(path: str) -> pd.DataFrame:
    return pd.read_json(path, orient="index", dtype={"fips": str})


def dataframe_from_rows(rows: List[List[str]]) -> pd.DataFrame:
    columns = ["fips",  # County fips code
               "NAME",  # County name
               "race_amer_indian_or_alaskan_native",  # Amer. Indian or Alaskan Native # noqa: E501
               "race_asian",  # Asian
               "race_black",  # Black or African American
               "race_native_hawaii_or_pacific_islander",  # Native Hawaii or Other Pacific Isl. # noqa: E501
               "race_white",  # White
               "race_multiracial",  # Multi-Racial
               "total",  # Total Participants
               "hispanic_or_latino"]  # Hispanic or Latino
    df = pd.DataFrame(data=rows, columns=columns)
    return df.set_index('fips')


def extract_columns_from_line(line: str) -> List[int]:
    # Split out a list like ["Total", "Infants", "1", "2", "3", "4"]
    str_list = line.split(sep=" ")
    return [int(s.replace(",", "")) for s in str_list[2:]]


def parse_wic_pdf(
        source_pdf_filepath: str,
        first_page_zero_indexed: int,
        last_page_zero_indexed: int) -> WICParticipation:

    # We'll use these regular expressions to find the lines we care about.
    # Find rows that start with Total (this includes Total Women, Total Infant
    # and Total Children rows)
    total_women_re = re.compile("Total Women")
    total_infants_re = re.compile("Total Infants")
    total_children_re = re.compile("Total Children")
    # It's not clear specifically what "LA Total" means, but these rows
    # contains the subtotal values for the specific County
    county_total_re = re.compile("LA Total")
    # find rows that start with three digits (these rows contain County ID and
    # name, example: 031 COOK)
    county_re = re.compile("[0-9][0-9][0-9]")

    women_rows = []
    infants_rows = []
    children_rows = []
    total_rows = []

    with pdfplumber.open(source_pdf_filepath) as pdf:

        # range() excludes the last value, so add 1 to include the last page
        for page_num in range(first_page_zero_indexed,
                              last_page_zero_indexed + 1):

            page = pdf.pages[page_num]

            # extract_text() adds spaces where the horizontal distance between
            # bits of text is greater than x_tolerance and adds newline
            # characters where the vertical distance between bits of text is
            # greater than y_tolerance.
            text = page.extract_text(x_tolerance=2, y_tolerance=0)

            county_info = ["", ""]  # fips, county name

            # iterate thru each line on a page
            for line in text.split("\n"):
                if county_re.match(line):
                    # We have to find the County information first because we
                    # insert it in every row maxsplit=1 because some counties
                    # have spaces in their name, example: Jo Daviess
                    county_info = (line.split(sep=" ", maxsplit=1))
                    county_info[0] = "17" + county_info[0]  # the pdf doesn't have the leading 17 indicating Illinois in the fips code # noqa: E501
                elif total_women_re.match(line):
                    women_rows.append(county_info + extract_columns_from_line(line))  # type: ignore # noqa: E501
                elif total_infants_re.match(line):
                    infants_rows.append(county_info + extract_columns_from_line(line))  # type: ignore # noqa: E501
                elif total_children_re.match(line):
                    children_rows.append(county_info + extract_columns_from_line(line))  # type: ignore # noqa: E501
                elif county_total_re.match(line):
                    total_rows.append(county_info + extract_columns_from_line(line))  # type: ignore # noqa: E501

    return WICParticipation(
        women=dataframe_from_rows(women_rows),
        infants=dataframe_from_rows(infants_rows),
        children=dataframe_from_rows(children_rows),
        total=dataframe_from_rows(total_rows))


def to_dict_for_wrapper(df: pd.DataFrame) -> Dict:
    new_df = df.drop('NAME', axis=1)  # we already include the county name elsewhere in the merged data # noqa: E501
    return new_df.to_dict(orient='index')


def wrapper_from_wic_participation(participation: WICParticipation) -> data.Wrapper:  # noqa: E501

    combined_data = data.Wrapper()
    combined_data.county["wic_participation_women_data"] = to_dict_for_wrapper(participation.women)  # noqa: E501
    combined_data.county["wic_participation_infants_data"] = to_dict_for_wrapper(participation.infants)  # noqa: E501
    combined_data.county["wic_participation_children_data"] = to_dict_for_wrapper(participation.children)  # noqa: E501
    combined_data.county["wic_participation_total_data"] = to_dict_for_wrapper(participation.total)  # noqa: E501

    numeric_column_names = ["race_amer_indian_or_alaskan_native",
                            "race_asian",
                            "race_black",
                            "race_native_hawaii_or_pacific_islander",
                            "race_white",
                            "race_multiracial",
                            "total",
                            "hispanic_or_latino"]

    combined_data.meta.data_bins["natural_breaks"] = {
        "wic_participation_women_data": data.calculate_natural_breaks_bins(participation.women, numeric_column_names),  # noqa: E501
        "wic_participation_infants_data": data.calculate_natural_breaks_bins(participation.infants, numeric_column_names),  # noqa: E501
        "wic_participation_children_data": data.calculate_natural_breaks_bins(participation.children, numeric_column_names),  # noqa: E501
        "wic_participation_total_data": data.calculate_natural_breaks_bins(participation.total, numeric_column_names),  # noqa: E501
    }
    combined_data.meta.data_bins["quantiles"] = {
        "wic_participation_women_data": data.calculate_quantiles_bins(participation.women, numeric_column_names),  # noqa: E501
        "wic_participation_infants_data": data.calculate_quantiles_bins(participation.infants, numeric_column_names),  # noqa: E501
        "wic_participation_children_data": data.calculate_quantiles_bins(participation.children, numeric_column_names),  # noqa: E501
        "wic_participation_total_data": data.calculate_quantiles_bins(participation.total, numeric_column_names),  # noqa: E501
    }

    return combined_data
