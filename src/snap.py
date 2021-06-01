import os
import sys
import pandas as pd
from typing import Any, Dict, Tuple, List, Callable
sys.path.append(os.path.abspath(''))
from src.census_response import county_fips  # noqa: E402
from src import data  # noqa: E402


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

    table_with_formatted_keys = {}
    for k in table:
        age_group = 'age_' + k.lower()[4:]
        table_with_formatted_keys[age_group] = table[k]

    return table_with_formatted_keys


def rename_columns(table: Dict[str, pd.DataFrame]) -> None:
    '''In-place renames the columns in each DataFrame to snake_case

    Arguments:
    table -- A dictionary mapping str keys to dataframes
    '''
    for k in table:
        table[k].columns = [
            'county',
            'race_white',
            'race_black',
            'race_native',
            'race_asian',
            'race_pacific',
            'race_hispaniclatino',
            'race_unknown']


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
        output[k] = table[k].to_dict(orient='index')
    return output


def make_bins(table: Dict[str, pd.DataFrame], bin_func: Callable) -> Dict:
    '''Internal utility to help make bins

    Arguments:
    table --  Dictionary mapping age group to DataFrame
    bin_func -- Function to make bins
    '''
    bin_dict = {}
    for age_group in table:
        df = table[age_group]
        numeric_columns = [column for column in df.columns if column != 'fips']
        bin_dict[age_group] = bin_func(df, numeric_columns)
    return bin_dict


def merge_snap_data(srcs: List[Tuple[str, str]]) -> data.Wrapper:
    '''Merges snap data into a data.Wrapper structure.

    Arguments:
    srcs -- A list of tuples where the first element is the year,
            second element is the path to the data source
    Returns:
    A data.Wrapper with the data sorted under county_data.snap_data.<year>
    '''
    merge_to: data.Wrapper = data.Wrapper()
    merge_to.county = {
        'snap_data': {}
    }
    merge_to.meta.data_bins = {
        'natural_breaks': {
            'snap_data': {}
        },
        'quantiles': {
            'snap_data': {}
        },
    }
    for src in srcs:
        year = src[0]
        table = load_xlsx(src[1])
        rename_columns(table)
        add_fips_column(table)
        table_dict = to_dict(table)

        for age_group in table_dict:
            for fips in table_dict[age_group]:
                if fips not in merge_to.county['snap_data']:
                    merge_to.county['snap_data'][fips] = dict()
                if year not in merge_to.county['snap_data'][fips]:
                    merge_to.county['snap_data'][fips][year] = dict()
                merge_to.county['snap_data'][fips][year][age_group] = table_dict[age_group][fips]  # noqa E501

        merge_to.meta.data_bins['natural_breaks']['snap_data'][year] = make_bins(table, data.calculate_natural_breaks_bins)  # noqa E501
        merge_to.meta.data_bins['quantiles']['snap_data'][year] = make_bins(table, data.calculate_quantiles_bins)  # noqa E501

    return merge_to
