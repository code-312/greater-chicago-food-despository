def main(blacklist = []):
    '''
    Reads excel/csv files into json format
    Excludes worksheets in blacklist
    '''
    import pandas as pd
    import os
    json_ls = list()
    f_walk = os.walk('data_folder')

    for subdir, dir, files in f_walk:
        for f in files:
            #pandas not only provides file reading functionality, but outputs in a single format
            #if performance requires, alternative packages may be implemented, 
            # but that will require additional processing after reading in the file
            fp = os.path.join(subdir, f)
            f_ext = f.split('.')[-1]
            table_ls = []
            if f_ext[:3] == 'xls':
                table = pd.read_excel(fp, sheet_name=None)
                if type(table) == dict:
                    for k in table:
                        if k not in blacklist:
                            table_ls.append((k+f,table[k]))
                        else: continue
            elif f_ext == 'csv':
                table_ls.append((f, pd.read_csv(fp)))
            elif f_ext == 'gitkeep':
                #for directory processing
                continue
            else:
                return Exception('File Type Not Supported')

            for t in table_ls:
                #table_ls is list of tuples
                #index 0: unique name
                #index 1: DataFrame
                #breakpoint()
                try:
                    table_json = table_to_json(t[1], t[0], blacklist=blacklist)
                except Exception as e:
                    print(e)
                    print(t)
                    print('-'*10)
                    table_json=[]
                json_ls.append(table_json)

    return(json_ls)


def determine_fips(df):
    '''
    Returns df with fips codes
    County name in df must be in the first column or named 'County Name'
    '''
    import pandas as pd
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
        #print(index, row)
        fip = fips[row[0]]
        df.iloc[index, -1] = fip

    return df


def table_to_json(df,  filename, blacklist=[]):
    '''
    Converts panda df to json format
    Checks for fips column, calls determine_fips if not present
    '''
    import pandas as pd
    import json

    # get county FIPs, if necessary
    columns = [c.lower() for c in df.columns]
    if 'fips' not in columns:
        # determine fips function
        df = determine_fips(df)
        # return merged dataframe

    #TODO nest data
    df = df.set_index('fips')
    df_json_str = df.to_json(orient='index')
    df_json_dict = json.loads(df_json_str)
    # breakpoint()
    df_values = [*df_json_dict.values()][0]

    final_dict = {k:{filename:v} for k,v in df_values.items()}

    return final_dict


if __name__ == '__main__':
    main(blacklist=['Key'])
