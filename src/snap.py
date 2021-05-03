import pandas as pd
from typing import Any


def load_excel(src: str) -> Any:
    table = pd.read_excel(src, sheet_name=None, engine='openpyxl')
    for k in table:
        table[k].dropna(axis=1, how='all', inplace=True)
        table[k].dropna(axis=0, how='any', inplace=True)
    return table


def rename_columns(table: dict[str, Any]) -> Any:
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


def add_fips_column(table: dict[str, Any]) -> Any:
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
