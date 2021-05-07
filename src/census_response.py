from src.config import CENSUS_KEY
import jenkspy
import json
import requests
import numpy as np
import pandas as pd
from numpyencoder import NumpyEncoder
from typing import Dict, List, Tuple
from src.data import GCFDData


def download_census_data(geo_ls=["zip", "county"]) -> None:
    '''
    Top level function to run the queries
    '''

    # Census tables
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'
    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

    # define race instance
    # Values name format: topic_property_subproperty...
    # B03002_003E: Does not include people of hispanic/latino origin
    race_variables = {'B03002_001E': 'race_total',
                      'B03002_005E': 'race_native',
                      'B03002_004E': 'race_black', 'B03002_003E': 'race_white',
                      'B03002_009E': 'race_twoplus_total',
                      'B03002_007E': 'race_pacific',
                      'B03002_008E': 'race_other', 'B03002_006E': 'race_asian',
                      'B03002_012E': 'race_hispaniclatino_total'}
    # race_functions = [processRaceData]
    # variable does not need to be defined, but it is for readability
    race = CensusRequest("race", detailed_table, race_variables)

    # define poverty instance
    poverty_variables = {'S1701_C01_001E': 'poverty_population_total',
                         'S1701_C02_001E': 'poverty_population_poverty',
                         'S1701_C02_002E': 'poverty_population_poverty_child'}
    # If additional subdivision are needed
    # 'S1701_C02_003E' = AGE!!Under 18 years!! Under 5 years!!
    # 'S1701_C02_004E' = AGE!!Under 18 years!! 5 to 17 years!!
    # poverty_functions = [processPovertyData]
    poverty = CensusRequest("poverty", subject_table, poverty_variables)

    get_and_save_census_data([race, poverty],
                             dump_output_path='final_jsons/df_dump.json',
                             merged_output_path='final_jsons/df_merged_json.json',  # noqa: E501
                             geo_ls=geo_ls)  


def get_census_response(table_url: str,
                        get_ls: List[str],
                        geo: str) -> List[List[str]]:
    '''
    Concatenates url string and returns response from census api query
    input:
        table_url (str): census api table url
        get_ls (ls): list of tables to get data from
        geo (str): geographic area and filter
    output:
        list of rows. first row is header:
            [NAME, <elements of get_ls>, state, county]
    '''
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={CENSUS_KEY}'
    response = requests.get(url)
    try:
        data_table = response.json()
    except json.JSONDecodeError:
        print("Error reading json from census response. Make sure you have a valid census key. Census Response: " + response.text)  # noqa: E501
        data_table = []
    return data_table


def df_to_json(data_metrics: Dict,
               data_bins: Dict,
               df_dict: Dict,
               dump_output_path: str = '',
               merged_output_path: str = '') -> None:
    '''
    Saves dataframe to file as json
    This format loads with load_df()
    '''
    class_json_dict = dict()
    # Add Meta Data Here (Bins, etc)
    class_json_dict['meta'] = {'data_metrics': data_metrics,
                               'data_bins': data_bins}

    if dump_output_path != "":
        fp = dump_output_path
        zip_dict = class_json_dict.copy()
        for k in df_dict:
            zip_dict[k] = df_dict[k].to_dict()

        with open(fp, 'w') as f:
            json.dump(zip_dict, f, separators=(',', ':'), cls=NumpyEncoder,
                      sort_keys=True)
        print(f'Data updated at {fp}')

    if merged_output_path != "":
        # determine metrics
        # Not sure we need this many loops, \
        # but seemed like a good idea at the time
        for geo in df_dict:
            geo_dict = dict()
            for geo_area in df_dict[geo].itertuples():
                geo_area_dict: Dict = {f'{m}_data': dict()
                                       for m in data_metrics.keys()}
                for name in geo_area._fields:
                    if name == "Index":
                        continue
                    for metric in data_metrics.keys():
                        metric_name = f'{metric}_data'
                        geo_area_dict[metric_name]
                        if metric in name:
                            geo_area_dict[metric_name][name] = getattr(
                                geo_area, name)
                            break
                    else:
                        geo_area_dict[name] = getattr(geo_area, name)
                geo_dict[geo_area.Index] = geo_area_dict
            class_json_dict[f'{geo}_data'] = geo_dict

        fp = merged_output_path
        with open(fp, 'w') as f:
            json.dump(class_json_dict, f, separators=(',', ':'),
                      cls=NumpyEncoder, sort_keys=True)
        print(f'Data updated at {fp}')


def nest_percentages(df: pd.DataFrame, total_col_str: str) -> tuple:
    '''
    Calculates percentages and removes NaN for dict conversion
    Returns calculated percent_df and series of dictionaries
    '''
    str_idx = total_col_str.find('_')
    metric = total_col_str[:str_idx]
    # divides df by total column to calculate percentages
    divide_by_total = lambda x: x / df[total_col_str]  # noqa: E731, E501
    # Casts to type float64 for numpy interoperability
    percent_df: pd.DataFrame = df.apply(divide_by_total) \
                                 .drop(total_col_str, axis=1) \
                                 .astype('float64') \
                                 .dropna()

    # Rounds to save space
    percent_df = np.round(percent_df, 6)

    # converts NAN to None, for proper JSON encoding
    # working_df = percent_df.where(pd.notnull(percent_df), None)
    working_df = percent_df

    return working_df


class CensusRequest:
    def __init__(self, metric: str, 
                 table: str, variables: Dict[str, str]) -> None:
        self.metric = metric
        self.table = table
        self.variables = variables


class CensusData:
    '''
    Stores and Updates Census Data in df_dict
    input:
        var_metrics (tuple):
            [0] metric name (str) e.g. race, poverty
            [1] variable (dict):
                Keys: Census Table Codes
                Values: Census Table Names/Aliases
        table (str): link to ACS5 Data Tables
        geo_ls (list): list of geographies to process
    Instructions:
        Create a class instance via input described above
        Use the get_data method to update CensusData.df_dict
            View dataframes: df_dict[key] (key='zip' or 'county')
        Save dataframe using CensusData.df_to_json()
            Default saves zipped by geo_code
            Set zip_df = False to save dataframes without processing
        Load dataframe using CensusData.load_df()
            Default loads unzipped saved file, described above
    '''

    def __init__(self, request: CensusRequest, geo: str):
        '''
        Initialized instance
        Adds metric to class set data_metrics
        '''
        self.metric = request.metric
        self.var_dict = request.variables
        self.var_keys = list(self.var_dict.keys())
        self.var_values = list(self.var_dict.values())
        self.table = request.table
        self.geo = geo

    def get_data(self) -> None:
        '''
        Calls getCensusResponse on each geography
        Sends response json to __panda_from_json function
        Returns list of DataFrames
        '''
        geo_dict = {'zip': 'zip code tabulation area:*',
                    'county': 'county:*&in=state:17'}
        geo_area = geo_dict[self.geo]
        self.response_json = get_census_response(self.table,
                                                 self.var_keys,
                                                 geo_area)
        self.df = self.__panda_from_json(self.response_json)
        data_obj = GCFDData(self.metric, self.df, path=tuple([self.geo]))
        self.name = data_obj.name
        self.fp = data_obj.fp
            
    def process_data(self) -> None:
        if self.metric == "race":
            self.__pd_process_race()
        elif self.metric == "poverty":
            self.__pd_process_poverty()

    def __panda_from_json(self,
                          response_json: List[List[str]]) -> pd.DataFrame:
        '''
        Called by getData method
        Updates CensusData.zip_df and returns response_df
        '''
        # Name Columns
        dict_values = list(self.var_dict.values())
        columns = [self.var_dict.get(header, header)
                   for header in response_json[0]]
        # Creates DF
        response_df = pd.DataFrame(response_json[1:], columns=columns)
        # adds types for performance and predictable method output
        string_df = response_df.astype('string')
        # ignore error to keep NAN values
        conversion_dict = {v: 'Int64' for v in dict_values}
        typed_df = string_df.astype(conversion_dict)
        # Processes geographies for output
        if self.geo == 'county':
            fip_series = typed_df.loc[:, 'state'] + typed_df.loc[:, 'county']
            fip_series.rename('FIPS', inplace=True)
            geo_df = pd.concat([typed_df, fip_series], axis=1)
            geo_df = geo_df.set_index('FIPS').drop(['state', 'county'], axis=1)
        elif self.geo == 'zip':
            # filter keeps Illinois zipcodes
            drop_ls = ['state'] if 'state' in typed_df else []
            drop_ls.append('NAME')
            geo_df = typed_df.set_index('zip code tabulation area') \
                .drop(drop_ls, axis=1) \
                .filter(regex='^(6[0-2])[0-9]+', axis=0)  # noqa: E501

        return geo_df

    def __pd_process_race(self) -> None:

        def majority(series):
            '''
            Returns majority race demographic
            for each geo_area
            If no majority, returns 'majority_minority'
            '''
            # indexes max value, returns NA for NA rows
            idx = series.idxmax()
            try:
                value = series[idx]
            except KeyError:
                # if NA row, idx = NA
                return None
            if value >= 0.5:
                return idx
            else:
                return 'majority_minority'

        # creates df using original columns
        # prevents conflicts with new columns
        # race_values = tuple(cls.data_metrics['race'].values())
        # breakpoint()
        race_df = self.df.loc[:, self.var_values]

        # divides df by race_total column to calculate percentages
        pct_df = create_percentages(race_df, 'race_total')  # noqa: E501
        pct_obj = GCFDData('percentages', pct_df,
                           path=tuple([self.geo, self.metric]))
        # breakpoint()
        # creates series of majority race demographics
        majority_series = pct_obj.df.apply(majority, axis=1)
        majority_df = pd.DataFrame(majority_series)
        GCFDData('majority', majority_df, path=tuple([self.geo, self.metric]))

    def __pd_process_poverty(self) -> None:
        poverty_df = self.df.loc[:, self.var_values]
        pct_df = create_percentages(poverty_df, 'poverty_population_total')
        pct_obj = GCFDData(f'percentages', pct_df,
                           path=tuple([self.geo, self.metric]))

        q_df = pct_obj.df.apply(np.quantile, q=(0, 0.25, 0.5, 0.75, 1))  # noqa: E501
        GCFDData.write_meta(q_df.to_dict())

        # create quantile bins using natural breaks algorithm.
        # bin_count could be increased to > 4 if needed.
        n_df = calculate_natural_breaks_bins(pct_obj.df, bin_count=4,
                                             column_names=["poverty_population_poverty",  # noqa: E501
                                                           "poverty_population_poverty_child"])  # noqa: E501

        GCFDData.write_meta(n_df.to_dict())


def search_table(table_json_ls: list, keyword_ls: list,
                 filter_function_ls: list) -> list:
    '''
    Filters variable tables by keyword and filter
    input:
        table_json_ls (response.json() list object):
                      list of lists from census variable table api
        keyword_ls (list):  list of keyword strings
                            keyword filter applied to the third element
                            of the input list (concept column)
        filter_function_ls (list): list of functions that filter
                                   table_json_ls with filter method
    output:
        return_json_ls (list): list, same format as table_json_ls, filtered
    '''
    return_json_ls = list()

    # runs filter for each function in filter_function_ls
    for f in filter_function_ls:
        table_json_ls = list(filter(f, table_json_ls))

    # adds rows with keyword(s) in concept column to return_json_ls
    for d in table_json_ls:
        try:
            for k in keyword_ls:
                # d[2] is the concept column, d[1] is the label column
                if k.lower() in d[2].lower() or k.lower() in d[1].lower():
                    continue
                else:
                    break
            else:
                return_json_ls.append(d)
        except IndexError:
            continue

    return return_json_ls


def county_fips(reverse=False) -> dict:
    '''
    Requests county fips from census API and returns list of IL county FIPS
    input: reverse (bool) reverses keys and values in output
    output: il_json (dict) {'county name': 'fip'}
    '''

    url = 'https://api.census.gov/data/2010/dec/sf1?get=NAME&for=county:*'

    response = requests.get(url)

    # filter for IL
    def il_county_filter(x):
        return x[1] == '17'

    response_json = response.json()

    if reverse:
        il_json = {county[1] + county[2]: county[0]
                   for county in response_json if il_county_filter(county)}
    else:
        il_json = {county[0]: county[1] + county[2]
                   for county in response_json if il_county_filter(county)}

    return il_json


def calculate_natural_breaks_bins(df: pd.DataFrame, bin_count: int,
                                  column_names: List[str]) -> Dict[str, List[float]]:  # noqa: 501
    """
    :param df: Pandas dataframe.
    :param bin_count: Number of bins used to classify data.
    :param column_names: dataframe column names used to calculate breaks
    :return: Dictionary of column name and list of bin cutoff limits.
    """
    bin_dict = {}
    for cn in column_names:
        column_data = df[cn].dropna().to_list()
        bin_dict[cn] = jenkspy.jenks_breaks(column_data, nb_class=bin_count)
    return pd.DataFrame(bin_dict)


def get_and_save_census_data(data_requests: List[CensusRequest],
                             dump_output_path: str = "",
                             merged_output_path: str = "",
                             geo_ls: List[str] = ["zip", "county"]) -> None:

    for request in data_requests:
        for geo in geo_ls:
            data = CensusData(request, geo)
            data.get_data()
            data.process_data()
