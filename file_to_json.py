def main():
    '''
    Reads excel/csv files into json format
    '''
    import pandas as pd
    json_ls = list()

    #Implement processing all files in data_folder
    #Challenge: relevant data may be on different worksheets
    fp = "data_folder/FoodInsecurityRates12.15.2020.xlsx"
    table = pd.read_excel(fp, "County")

    json_ls.append(table)
    print(json_ls)
    return(json_ls)


def determine_fips(df):
    '''
    Returns df with fips codes
    County name in df must be in the first column or named 'County Name'
    '''
    import pandas as pd
    from census_response import county_fips

    fips = county_fips()
    # verify county column
    # Moves properly named column to first column
    first_column_name = table.iloc[:, 0].name
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


def table_to_json(df):
    '''
    Converts panda df to json format
    Checks for fips column, calls determine_fips if not present
    '''
    import pandas as pd

    # get county FIPs, if necessary
    columns = [c.lower() for c in table.columns]
    if 'fips' not in columns:
        # determine fips function
        table = determine_fips(table)
        # return merged dataframe

    df = df.set_index('fips')
    df_json = df.to_json(orient='index')
    return table_json


if __name__ == '__main__':
    main()
