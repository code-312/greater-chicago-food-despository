import os
import sys
import pandas as pd
from typing import Any, Dict, Tuple, List
sys.path.append(os.path.abspath(''))
from src.census_response import county_fips  # noqa: E402


def load_xlsx(src: str) -> Dict[str, pd.DataFrame]:
    '''Loads Excel worksheets into DataFrames

    Arguments:
    src -- path to an xlsx file

    Returns:
    A dictionary mapping worksheet names to DataFrames
    '''
    table = pd.read_excel(src, sheet_name=None, engine='openpyxl')
    for k in table:
        # drop empty rows (i.e. all values are NaN)
        table[k].dropna(axis=1, how='all', inplace=True)
        # drop empty columns (i.e. any value in column is NaN)
        table[k].dropna(axis=0, how='any', inplace=True)

        # drop last row (contains column sums)
        table[k] = table[k][table[k]['Unnamed: 0'] != 'Sum:']

        # ensure we're indexing from 0
        table[k].reset_index(inplace=True)

        # drop column of old indices
        table[k].drop(table[k].columns[0], axis=1, inplace=True)
    return table


def rename_columns(table: Dict[str, pd.DataFrame]) -> None:
    '''In-place renames the columns in each DataFrame to snake_case

    Arguments:
    table -- A dictionary mapping str keys to dataframes
    '''
    for k in table:
        columns = []
        columns.append('county')
        columns.append('race_white')
        columns.append('race_black')
        columns.append('race_native')
        columns.append('race_asian')
        columns.append('race_pacific')
        columns.append('race_hispaniclatino')
        columns.append('race_unknown')
        table[k].columns = columns


def add_fips_column(table: Dict[str, pd.DataFrame]) -> None:
    '''Adds a column in-place to each DataFrame where each row value is
    the FIPS code for the county named in the 'county' column

    Arguments:
    table -- A dictionary mapping str keys to DataFrames
    '''
    fips = county_fips()
    # We're going to make a separate dictionary where the keys are just
    # the county name in all caps. Note that we're trimming out spaces
    # as well to account for e.g. DE WITT vs. DEWITT, which is written
    # both ways depending on the data source
    abbr_fips = dict()
    for k in fips:
        abbr_key = k.upper().replace(' COUNTY, ILLINOIS', '').replace(' ', '')
        abbr_fips[abbr_key] = fips[k]

    # Now that we have the new dictionary, populate the fips column
    for k in table:
        table[k]['fips'] = None
        for index, row in table[k].iterrows():
            fip = abbr_fips[row[0].replace(' ', '')]
            table[k].iloc[index, -1] = fip

        # Set index to fips column
        table[k].set_index('fips', inplace=True)

        # drop column of county names
        table[k].drop('county', axis=1, inplace=True)


def to_dict(table: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Dict[str, Any]]]:  # noqa E501
    '''Combines several dataframes into a single dictionary structure.

    Arguments:
    table -- A dictionary mapping str keys to DataFrames

    Returns:
    A dictionary with the structure:
    {
        <age group>: {
            <fips>: {
                "race_white": 0
                ...
                "race_unknown": 0
            }
        }
    }
    '''
    output = dict()
    for k in table:
        age_group = 'age_' + k.lower()[4:]
        as_dict = table[k].to_dict(orient='index')
        output[age_group] = as_dict
    return output


def merge_snap_data(srcs: List[Tuple[str, str]], merge_to: Dict[str, Any]) -> Dict[str, Any]:  # noqa E501
    '''Merges snap data into an existing dictionary structure.

    Arguments:
    srcs -- A list of tuples where the first element is the year,
            second element is the path to the data source
    merge_to -- A dictionary structure countaining a key named 'county_data.'
                Will be modified in-place.

    Returns:
    The modified dictionary (i.e. merge_to)
    '''
    for src in srcs:
        year = src[0]
        table = load_xlsx(src[1])
        rename_columns(table)
        add_fips_column(table)
        table_dict = to_dict(table)
        for fips in merge_to['county_data']:
            for age_group in table_dict:
                if 'snap_data' not in merge_to['county_data'][fips]:
                    merge_to['county_data'][fips]['snap_data'] = dict()
                if year not in merge_to['county_data'][fips]['snap_data']:
                    merge_to['county_data'][fips]['snap_data'][year] = dict()
                merge_to['county_data'][fips]['snap_data'][year][age_group] = table_dict[age_group][fips]  # noqa E501
    return merge_to
