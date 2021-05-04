import os
import sys
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
        table[k].drop(table[k].tail(1).index, inplace=True)

        # ensure we're indexing from 0
        table[k].reset_index(inplace=True)

        # drop column of old indices
        table[k].drop(table[k].columns[0], axis=1, inplace=True)
    return table


def rename_columns(table: Dict[str, Any]) -> Any:
    for k in table:
        age_group = 'age_' + k.lower()[4:]
        columns = []
        columns.append('county')
        columns.append('race_white_{}'.format(age_group))
        columns.append('race_black_{}'.format(age_group))
        columns.append('race_native_{}'.format(age_group))
        columns.append('race_asian_{}'.format(age_group))
        columns.append('race_pacific_{}'.format(age_group))
        columns.append('race_hispaniclatino_{}'.format(age_group))
        columns.append('race_unknown_{}'.format(age_group))
        table[k].columns = columns
    pass


def add_fips_column(table: Dict[str, Any]) -> Any:
    fips = county_fips()
    abbr_fips = dict()
    for k in fips:
        abbr_key = k.upper().replace(' COUNTY, ILLINOIS', '').replace(' ', '')
        abbr_fips[abbr_key] = fips[k]
    for k in table:
        table[k]['fips'] = None
        for index, row in table[k].iterrows():
            fip = abbr_fips[row[0].replace(' ', '')]
            table[k].iloc[index, -1] = fip
        table[k].set_index('fips', inplace=True)
    pass


def merge_snap_data(srcs: list) -> None:
    for src in srcs:
        table = load_excel(src)
        rename_columns(table)
        add_fips_column(table)
        print(table)
    pass


if __name__ == '__main__':
    merge_snap_data(['data_folder/SNAP_2019.xlsx'])
