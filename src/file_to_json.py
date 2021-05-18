import os
import xlrd
import pandas as pd
from typing import Tuple, List, Dict
from src.census_response import county_fips
from src import data


def file_to_json(input_dir: str, output_dir: str, blacklist: List[str] = []) -> None:  # noqa: E501
    '''
    Reads excel/csv files into json format
    Excludes worksheets in blacklist
    '''
    table_ls = files_to_dataframes(input_dir, blacklist)
    dataframes_to_json_files(table_ls, output_dir)


def file_to_wrapper(input_dir: str, blacklist: List[str] = []) -> data.Wrapper:  # noqa: E501
    table_ls = files_to_dataframes(input_dir, blacklist)
    combined_data = data.Wrapper()
    for pair in table_ls:
        combined_data.add(data.from_county_dataframe(pair[1]))
    return combined_data


def files_to_dataframes(input_dir: str, blacklist: List[str] = []) -> List[Tuple[str, pd.DataFrame]]:  # noqa: E501
    table_ls: List[Tuple[str, pd.DataFrame]] = []  # unique name, DataFrame

    f_walk = os.walk(input_dir)

    for subdir, _, files in f_walk:
        for f in files:
            fp = os.path.join(subdir, f)
            table_ls = table_ls + file_to_dataframes(fp, blacklist)

    normalized_tables = [(pair[0], normalize_dataframe(pair[1])) for pair in table_ls]  # noqa: E501

    return normalized_tables


def file_to_dataframes(filepath: str, blacklist: List[str] = []) -> List[Tuple[str, pd.DataFrame]]:  # noqa: E501
    '''Returns list of (unique name, DataFrame)'''

    directory, filename_with_extension = os.path.split(filepath)
    f_name, f_ext = os.path.splitext(filename_with_extension)

    if f_ext[:4] == '.xls':
        # openpyxl can open .xlsx but not .xls
        # xlrd can open .xls but not .xlsx
        if f_ext == '.xlsx':
            engine = 'openpyxl'
        else:
            engine = 'xlrd'
        try:
            table = pd.read_excel(filepath, sheet_name=None, engine=engine)
        except xlrd.biffh.XLRDError as e:
            print(e)
            raise Exception("Error reading {0}. Close the file if you have it open.".format(filepath))  # noqa: E501
        table_ls: List[Tuple[str, pd.DataFrame]] = []
        if type(table) == dict:
            for k in table:
                if k not in blacklist:
                    table_ls.append((k+f_name, table[k]))
                else:
                    continue
        return table_ls
    elif f_ext == '.csv':
        return [(f_name, pd.read_csv(filepath))]
    else:
        # need to account for e.g. .gitkeep and PDF files
        print('Skipping unsupported file {}'.format(filepath))
        return []


def dataframes_to_json_files(tables: List[Tuple[str, pd.DataFrame]], output_dir: str) -> None:  # noqa: E501
    for t in tables:
        try:
            table_to_json(t[1], os.path.join(output_dir, t[0] + '.json'))
        except Exception as e:
            print(e)
            print(t)
            print('-'*10)


def determine_fips(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns df with fips codes
    County name in df must be in the first column or named 'County Name'
    '''

    fips: Dict[str, str] = county_fips()
    # Verifies county column
    # Moves properly named column to first column
    first_column_name = df.iloc[:, 0].name
    cols = df.columns
    default_name = 'County Name'
    if default_name in cols and default_name != first_column_name:
        col_ls = cols.tolist()
        col_ls.remove(default_name)
        col_ls.insert(0, default_name)
        df = df[col_ls]
    else:
        df = df.rename(columns={first_column_name: default_name})
    # add fip column, will be last column (-1)
    df['fips'] = None

    # update fip column with fip codes
    for index, row in df.iterrows():
        # print(index, row)
        fip = fips[row[0]]
        df.iloc[index, -1] = fip

    return df


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    '''Tries to add a fips column index if it's missing'''
    columns = [c.lower() for c in df.columns]
    if 'fips' not in columns:
        df = determine_fips(df)
    df = df.set_index('fips')
    return df


def table_to_json(df: pd.DataFrame, filepath: str) -> None:
    '''
    Converts panda df to json format
    '''
    import json

    json_str = df.to_json(orient='index')
    # normalize line endings to LF
    json_str = json_str.replace('\\r\\n', '\\n').replace('\\r', '\\n')
    final_json = json.loads(json_str)
    with open(filepath, 'w') as json_file:
        # separators option here minimizes whitespace
        json.dump(final_json, json_file, separators=(',', ':'))


if __name__ == '__main__':
    file_to_json('data_folder', 'final_jsons', blacklist=['Key'])
