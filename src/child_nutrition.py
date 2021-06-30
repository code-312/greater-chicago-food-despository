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
        table[k].dropna(axis=0, how='all', inplace=True)

        print(table[k])

        # ensure we're indexing from 0
        table[k].reset_index(inplace=True)

        # drop column of old indices
        table[k].drop(table[k].columns[0], axis=1, inplace=True)

        print(table[k])

    return table 

def rename_columns(table: Dict[str, pd.DataFrame]) -> None:
    '''In-place renames the columns in each DataFrame to snake_case

    Arguments:
    table -- A dictionary mapping str keys to dataframes
    '''
    for k in table:
        table[k].columns = [
            'county',
            'breakfast_count',
            'lunch_count',
            'sfsp_count',
            'afterschool_meals_count']

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
            fip = abbr_fips[row[0].replace(' ', '').upper()]
            table[k].iloc[index, -1] = fip

        # Set index to fips column
        table[k].set_index('fips', inplace=True)

        # drop column of county names
        table[k].drop('county', axis=1, inplace=True)

        print(table[k])


def to_dict(table: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Dict[str, Any]]]:  # noqa E501
    '''Combines several dataframes into a single dictionary structure.

    Arguments:
    table -- A dictionary mapping str keys to DataFrames

    Returns:
    A dictionary with the structure:
    {
        <fips>: {
            "breakfast_count": 0,
            "lunch_count": 0,
            "sfsp_count": 0,
            "afterschool_meals_count": 0
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
    for k in table:
        df = table[k]
        numeric_columns = [column for column in df.columns if column != 'fips']
        bin_dict[k] = bin_func(df, numeric_columns)
    return bin_dict


def merge_child_nutrition_data(srcs: List[Tuple[str, str]]) -> data.Wrapper:
    '''Merges child nutrition data into a data.Wrapper structure.

    Arguments:
    srcs -- A list of tuples where the first element is the year,
            second element is the path to the data source
    Returns:
    A data.Wrapper with the data sorted under county_data.child_nutrition.<year>
    '''
    merge_to: data.Wrapper = data.Wrapper()
    merge_to.county = {
        'child_nutrition_data': {}
    }
    merge_to.meta.data_bins = {
        'natural_breaks': {
            'child_nutrition_data': {}
        },
        'quantiles': {
            'child_nutrition_data': {}
        },
    }
    for src in srcs:
        year = src[0]
        table = load_xlsx(src[1])
        rename_columns(table)
        add_fips_column(table)
        table_dict = to_dict(table)

        for sheet in table_dict:
            for fips in table_dict[sheet]:
                if fips not in merge_to.county['child_nutrition_data']:
                    merge_to.county['child_nutrition_data'][fips] = dict()
                if year not in merge_to.county['child_nutrition_data'][fips]:
                    merge_to.county['child_nutrition_data'][fips][year] = dict()
                merge_to.county['child_nutrition_data'][fips][year] = table_dict[sheet][fips]  # noqa E501

        merge_to.meta.data_bins['natural_breaks']['child_nutrition_data'][year] = make_bins(table, data.calculate_natural_breaks_bins)  # noqa E501
        merge_to.meta.data_bins['quantiles']['child_nutrition_data'][year] = make_bins(table, data.calculate_quantiles_bins)  # noqa E501

    return merge_to

if __name__ == '__main__':
    merge_child_nutrition_data([('2019', 'data_folder/child_nutrition/child_meals_2019.xlsx')])  # noqa: E501