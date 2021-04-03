import re
import pdfplumber
import pandas as pd


'''
GCFD staff provided a pdf illinois_wic_data_january_2021.pdf which contains WIC
data for 96 out of 102 IL Counties. We do not know why some counties are
missing. Data is for the month of January year 2021. wic.py reads thru each
line of each page of the pdf looking for lines that contain the data we want
and then saves that data to a dataframe. GCFD staff also requested a .csv
version of the data'''


def read_wic_data() -> None:
    # PDF has 97 pages. Skip page 0 because it shows Statewide totals which we
    # don't need
    parse_wic_pdf(
        "data_folder/illinois_wic_data_january_2021.pdf",
        "final_jsons/wic.csv",
        1,
        96)


def parse_wic_pdf(
        source_pdf_filepath: str,
        destination_csv_filepath: str,
        first_page_zero_indexed: int,
        last_page_zero_indexed: int) -> None:

    # We'll use these regular expressions to find the lines we care about.
    # Find rows that start with Total (this includes Total Women, Total Infant
    # and Total Children rows)
    total_re = re.compile("Total")
    # It's not clear specifically what "LA Total" means, but these rows
    # contains the subtotal values for the specific County
    county_total_re = re.compile("LA Total")
    # find rows that start with three digits (these rows contain County ID and
    # name, example: 031 COOK)
    county_re = re.compile(r"\d\d\d")

    rows = []

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

            # iterate thru each line on a page
            for line in text.split("\n"):
                if county_re.match(line):
                    # We have to find the County information first because we
                    # insert it in every row maxsplit=1 because some counties
                    # have spaces in their name, example: Jo Daviess
                    county = (line.split(sep=" ", maxsplit=1))
                elif total_re.match(line):
                    # Split out a list like ["Total", "Women", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    rows.append(county + new_line)

                elif county_total_re.match(line):
                    # Split out a list like ["LA", "Total", 1, 2, 3, 4]
                    new_line = (line.split(sep=" "))
                    rows.append(county + new_line)

    column_names = ["County_ID",
                    "County",
                    "WIC1",
                    "WIC2",
                    "Amer. Indian or Alaskan Native",
                    "Asian",
                    "Black or African American",
                    "Native Hawaii or Other Pacific Isl.",
                    "White",
                    "Multi-Racial",
                    "Total Participants",
                    "Hispanic or Latino"]

    data = pd.DataFrame(rows, columns=column_names)

    # Currently the data looks like this:
    # WIC1      WIC2       etc
    # Total     Women
    # Total     Children
    # LA        Total

    # We want to combine WIC1 and WIC2 columns into new column called WIC
    # which will contain values such as "Total Women" "Total Children"
    # "Total Infants" and "LA Total"
    data.insert(2, "WIC", (data["WIC1"] + " " + data["WIC2"]))

    # delete WIC1 and WIC 2 columns
    data.drop(['WIC1', 'WIC2'], axis=1, inplace=True)

    data.to_csv(destination_csv_filepath, index=False)
