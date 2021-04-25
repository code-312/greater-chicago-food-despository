import os
import re
import pdfplumber
import pandas as pd
from typing import List, Dict


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


def read_wic_data(always_run: bool = False) -> None:

    input_file_path = "data_folder/illinois_wic_data_january_2021.pdf"
    output_file_path = "final_jsons/wic.csv"

    if always_run or not is_up_to_date(input_file_path, output_file_path):
        # PDF has 97 pages. Skip page 0 because it shows Statewide totals
        # which we don't need
        parse_wic_pdf(
            input_file_path,
            output_file_path,
            1,
            96)


def dataframe_from_rows(rows: List[List[str]]) -> pd.DataFrame:
    columns = ["fips",  # County fips code
               "NAME",  # County name
               "race_amer_indian_or_alaskan_native",  # Amer. Indian or Alaskan Native
               "race_asian",  # Asian
               "race_black",  # Black or African American
               "race_native_hawaii_or_pacific_islander",  # Native Hawaii or Other Pacific Isl.
               "race_white",  # White
               "race_multiracial",  # Multi-Racial
               "total",  # Total Participants
               "hispanic_or_latino"]  # Hispanic or Latino
    return pd.DataFrame(data=rows, columns=columns)



def parse_wic_pdf(
        source_pdf_filepath: str,
        destination_csv_filepath: str,
        first_page_zero_indexed: int,
        last_page_zero_indexed: int) -> None:

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
                    county_info[0] = "17" + county_info[0]  # the pdf doesn't have the leading 17 indicating Illinois in the fips code
                elif total_women_re.match(line):
                    # Split out a list like ["Total", "Women", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    women_rows.append(county_info + new_line[2:])
                elif total_infants_re.match(line):
                    # Split out a list like ["Total", "Infants", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    infants_rows.append(county_info + new_line[2:])
                elif total_children_re.match(line):
                    # Split out a list like ["Total", "Children", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    children_rows.append(county_info + new_line[2:])
                elif county_total_re.match(line):
                    # Split out a list like ["LA", "Total", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    total_rows.append(county_info + new_line[2:])

    for row in women_rows:
        assert len(row) == 10, "women " + row[1]

    for row in children_rows:
        assert len(row) == 10, "children " + row[1]

    for row in infants_rows:
        assert len(row) == 10, "infants " + row[1]

    for row in total_rows:
        assert len(row) == 10, "total " + row[1]

    dataframes: Dict[str, pd.DataFrame] = {
        "wic_participation_women_data": dataframe_from_rows(women_rows),
        "wic_participation_infants_data": dataframe_from_rows(infants_rows),
        "wic_participation_children_data": dataframe_from_rows(children_rows),
        "wic_participation_total_data": dataframe_from_rows(total_rows),
    }

    dataframes["wic_participation_women_data"].to_csv(destination_csv_filepath, index=False)

