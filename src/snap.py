import os
import sys
import json
import pandas as pd
from typing import Any, Dict
sys.path.append(os.path.abspath(''))
from src.census_response import county_fips  # noqa: E402


def load_excel(src: str) -> Any:
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


def rename_columns(table: Dict[str, Any]) -> None:
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


def add_fips_column(table: Dict[str, Any]) -> None:
    fips = county_fips()
    # We're going to make a separate dictionary where the keys are just
    # the county name in all caps. Note that we're trimming out spaces
    # as well to account for e.g. DE WITT vs. DEWITT
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


def to_dict(table: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    output = dict()
    for k in table:
        age_group = 'age_' + k.lower()[4:]
        as_dict = table[k].to_dict(orient='index')
        output[age_group] = as_dict
    return output


# srcs is a list of tuples where the first element is the year,
# second element is the path to the data source
def merge_snap_data(srcs: list[tuple[str, str]], merge_to: Dict[str, Any]) -> Dict[str, Any]:  # noqa E501
    for src in srcs:
        table = load_excel(src[1])
        rename_columns(table)
        add_fips_column(table)
        table_dict = to_dict(table)
        for fips in merge_to['county_data']:
            for age_group in table_dict:
                if 'snap_data' not in merge_to['county_data'][fips]:
                    merge_to['county_data'][fips]['snap_data'] = dict()
                if src[0] not in merge_to['county_data'][fips]['snap_data']:
                    merge_to['county_data'][fips]['snap_data'][src[0]] = dict()
                merge_to['county_data'][fips]['snap_data'][src[0]][age_group] = table_dict[age_group][fips]  # noqa E501
    return merge_to


if __name__ == '__main__':
    with open('final_jsons/df_merged_with_insecurity.json') as merged:
        merged_data = json.load(merged)
    with_snap = merge_snap_data([('2019', 'data_folder/SNAP_2019.xlsx'),('2020', 'data_folder/SNAP_2020.xlsx')], merged_data)  # noqa E501
    with open('final_jsons/df_merged_with_insecurity_and_snap.json','w+') as new_merged:  # noqa E501
        json.dump(with_snap, new_merged)
