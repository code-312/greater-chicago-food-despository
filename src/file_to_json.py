import os
import sys
sys.path.append(os.path.abspath(''))
import pandas as pd

def file_to_json(input_dir, output_dir, blacklist=[]):
    '''
    Reads excel/csv files into json format
    Excludes worksheets in blacklist
    '''
    f_walk = os.walk(input_dir)

    for subdir, _, files in f_walk:
        for f in files:
            # pandas not only provides file reading functionality,
            # but outputs in a single format
            # if performance requires, other packages may be implemented,
            # that may require additional processing after reading in the file
            fp = os.path.join(subdir, f)
            # using splitext allows '.' to appear in the filename
            f_name, f_ext = os.path.splitext(f) 
            table_ls = []
            if f_ext[:4] == '.xls':
                table = pd.read_excel(fp, sheet_name=None, engine='openpyxl')
                if type(table) == dict:
                    for k in table:
                        if k not in blacklist:
                            table_ls.append((k+f_name, table[k]))
                        else:
                            continue
            elif f_ext == '.csv':
                table_ls.append((f_name, pd.read_csv(fp)))
            else:
                # need to account for e.g. .gitkeep and PDF files
                print('Skipping unsupported file {}'.format(f))
                continue

            for t in table_ls:
                # table_ls is list of tuples
                # index 0: unique name
                # index 1: DataFrame
                try:
                    table_to_json(t[1], os.path.join(output_dir, t[0] + '.json'))
                except Exception as e:
                    print(e)
                    print(t)
                    print('-'*10)


def determine_fips(df):
    '''
    Returns df with fips codes
    County name in df must be in the first column or named 'County Name'
    '''
    from census_response import county_fips

    fips = county_fips()
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


def table_to_json(df, filepath):
    '''
    Converts panda df to json format
    Checks for fips column, calls determine_fips if not present
    '''

    # get county FIPs, if necessary
    columns = [c.lower() for c in df.columns]
    if 'fips' not in columns:
        # determine fips function
        df = determine_fips(df)
        # return merged dataframe
    
    df = df.set_index('fips')
    df.to_json(filepath, orient='index')


if __name__ == '__main__':
    file_to_json('data_folder', 'final_jsons', blacklist=['Key'])
