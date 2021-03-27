import re
import pdfplumber
import pandas as pd


'''
GCFD staff provided a pdf IWIC.pdf which contains WIC data for 96 out of 102 IL Counties. We do not know why some counties
are missing. Data is for the month of January year 2021. WIC.py reads thru each line of each page of the pdf looking
 for lines that contain the data we want and then saves that data to a dataframe. GCFD staff also requested a .csv version
 of the data'''

def read_wic_data():
    # use regular expression matching to find lines that start with certain words and save as variables:
    # find rows that start with Total (this includes Total Women, Total Infant and Total Children rows)
    Total_re = re.compile("Total")
    # It's not clear specifically what "LA Total" means, but these rows contains the subtotal values for the specific County
    County_Total_re = re.compile("LA Total")
    # find rows that start with three digits (these rows contain County ID and name, example: 031 COOK)
    County_re = re.compile(r"\d\d\d")

    # define column names
    # readable column names
    column_names = ["County_ID", "County", "WIC1", "WIC2", "Amer. Indian or Alaska Native",
                    "Asian", "Black or African American", "Native Hawaii or Other Pacific Isl.",
                    "White", "Multi Racial", "Total_Participants", "Hispanic_Latino"]

    # create empty data frame with column names
    data = pd.DataFrame(columns=column_names)

    # filepath to the PDF we want to read data from
    filepath = "data_folder/illinois_wic_data_january_2021.pdf"

    with pdfplumber.open(filepath) as pdf:
    
        # read each page of the pdf pages 1 thru 97. Skip page 0 because it shows Statewide totals which we don't need
        for p in range(1, 97):
            page = pdf.pages[p]

            # extract_text() adds spaces where the horizontal distance between bits of text is greater than x_tolerance
            # and adds newline characters where the vertical distance between bits of text is greater than y_tolerance.
            text = page.extract_text(x_tolerance=2, y_tolerance=0)

            # iterate thru each line on a page
            for line in text.split("\n"):
                # find the county info and save as variable County
                # maxsplit=1 because some counties have spaces in their name
                if County_re.match(line):
                    County = (line.split(sep=" ", maxsplit=1))
                # finds the lines that start with Total
                # appends to data
                elif Total_re.match(line):
                    new_line = (line.split(sep=" "))
                    new_line = County + new_line
                    data = data.append(pd.Series(new_line, index=data.columns), ignore_index=True)
                # finds lines that start with LA
                # appends to data
                elif County_Total_re.match(line):
                    new_line = (line.split(sep=" "))
                    new_line = County + new_line
                    data = data.append(pd.Series(new_line, index=data.columns), ignore_index=True)

    # Currently column WIC1 contains values "Total" and "LA" and WIC2 contains values such as "Women" "Children"
    # We want to combine WIC1 and WIC2 columns into new column called WIC which will contain values such as "Total Women"
    # "Total Children" "Total Infants" and "LA Total"
    data.insert(2, "WIC", (data["WIC1"] + " " + data["WIC2"]))

    # delete WIC1 and WIC 2 columns
    data.drop(['WIC1', 'WIC2'], axis=1, inplace=True)

    # GCFD asked that we save the data to a csv and provide it to them
    # save as csv
    csv_filepath = "final_jsons/wic.csv"
    data.to_csv(csv_filepath, index=False)
