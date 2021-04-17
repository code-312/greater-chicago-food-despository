from src.config import CENSUS_KEY
import jenkspy
import json
import requests
import numpy as np
import pandas as pd
from numpyencoder import NumpyEncoder
from typing import Dict, List


def get_census_response(table_url: str, get_ls: List[str], geo: str):
    '''
    Concatenates url string and returns response from census api query
    input:
        table_url (str): census api table url
        get_ls (ls): list of tables to get data from
        geo (str): geographic area and filter
    output:
        response (requests.response): api response
    '''
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={CENSUS_KEY}'
    # print(f"Calling for {geo}: {get_ls}")
    response = requests.get(url)
    # print(f"{response} Received")
    return response


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
    df_dict = {}
    data_metrics = dict()
    data_bins = dict()

    def __init__(self, var_metrics: tuple,
                 table: str, geo_ls: list = ["zip", "county"]):
        '''
        Initialized instance
        Adds metric to class set data_metrics
        '''
        self.metric = var_metrics[0]
        self.var_dict = var_metrics[1]
        self.data_metrics[self.metric] = self.var_dict
        self.table = table
        self.geo_ls = geo_ls

    def get_data(self) -> List[pd.DataFrame]:
        '''
        Calls getCensusResponse on each geography
        Sends response json to __panda_from_json function
        Returns list of DataFrames
        '''
        geo_dict = {'zip': 'zip code tabulation area:*',
                    'county': 'county:*&in=state:17'}
        get_ls = list(self.var_dict.keys())
        df_ls = []
        for g in self.geo_ls:
            response = get_census_response(self.table, get_ls, geo_dict[g])
            self.response_json = response.json()
            df = self.__panda_from_json(self.response_json, g)
            df_ls.append(df)
        return df_ls

    @classmethod
    def process_data(cls, save=False):
        cls.__pd_process_race()
        cls.__pd_process_poverty()

        if save:
            cls.df_to_json(both=True)

    def __panda_from_json(self, response_json, geo):
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
        if geo == 'county':
            fip_series = typed_df.loc[:, 'state'] + typed_df.loc[:, 'county']
            fip_series.rename('FIPS', inplace=True)
            geo_df = pd.concat([typed_df, fip_series], axis=1)
            geo_df = geo_df.set_index('FIPS').drop(['state', 'county'], axis=1)
        elif geo == 'zip':
            # filter keeps Illinois zipcodes
            drop_ls = ['state'] if 'state' in typed_df else []
            drop_ls.append('NAME')
            geo_df = typed_df.set_index('zip code tabulation area') \
                .drop(drop_ls, axis=1) \
                .filter(regex='^(6[0-2])\d+', axis=0)  # noqa: W605, E501

        # checks if df exists
        class_df = self.df_dict.get(geo, pd.DataFrame())
        if not (class_df.empty):
            # Removes NAME to avoid conflict
            geo_df = geo_df.drop(
                ['NAME'], axis=1) if 'NAME' in class_df.columns else geo_df
            try:
                self.df_dict[geo] = class_df.join(geo_df, how='outer')
            except Exception as e:
                print(e)
                print("Make sure the column names are unique")
        else:
            self.df_dict[geo] = geo_df

        return geo_df

    @classmethod
    def df_to_json(cls, zip_df=True, both=False):
        '''
        Saves df to file
        Default: zips dataframe by geo_code
        Both: overrides zip_df, saves both
        Otherwise: saves df.to_json() in dictionary to json
            This format loads with load_df()
        '''
        zip_df = False if both else zip_df
        class_json_dict = dict()
        # Add Meta Data Here (Bins, etc)
        class_json_dict['meta'] = {'data_metrics': cls.data_metrics,
                                   'data_bins': cls.data_bins}
        if not (zip_df):
            fp = 'final_jsons/df_dump.json'
            zip_dict = class_json_dict.copy()
            for k in cls.df_dict:
                zip_dict[k] = cls.df_dict[k].to_dict()

            with open(fp, 'w') as f:
                json.dump(zip_dict, f, separators=(',', ':'),
                          cls=NumpyEncoder)
            if not (both):
                return fp

        # determine metrics
        # Not sure we need this many loops, \
        # but seemed like a good idea at the time
        for geo in cls.df_dict:
            geo_dict = dict()
            for geo_area in cls.df_dict[geo].itertuples():
                geo_area_dict = {f'{m}_data': dict()
                                 for m in cls.data_metrics.keys()}
                for name in geo_area._fields:
                    if name == "Index":
                        continue
                    for metric in cls.data_metrics.keys():
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

        fp = 'final_jsons/df_merged_json.json'
        with open(fp, 'w') as f:
            json.dump(class_json_dict, f, separators=(',', ':'),
                      cls=NumpyEncoder, sort_keys=True)

        fp = 'final_jsons/' if both else fp
        print(f'Data updated at {fp}')
        return fp

    @classmethod
    def load_df(cls, fp='final_jsons/df_dump.json'):
        '''
        Loads df_dict from file saved from df_to_json
        '''
        with open(fp) as f:
            load_df = json.load(f)

        cls.df_dict = dict()

        for k in load_df:
            if k == 'meta':
                cls.data_metrics = load_df[k]['data_metrics']
                continue
            v = pd.DataFrame(load_df[k])
            cls.df_dict[k] = v

        return None

    @classmethod
    def get_data_values(cls, metric_name):
        return tuple(cls.data_metrics[metric_name].values())

    @classmethod
    def __nest_percentages(cls, df, total_col_str):
        '''
        Calculates percentages and removes NaN for dict conversion
        Returns calculated percent_df and series of dictionaries
        '''
        str_idx = total_col_str.find('_')
        metric = total_col_str[:str_idx]
        # divides df by total column to calculate percentages
        divide_by_total = lambda x: x / df[total_col_str]  # noqa: E731, E501
        # Casts to type float64 for numpy interoperability
        percent_df = df.apply(divide_by_total) \
                       .drop(total_col_str, axis=1) \
                       .astype('float64')
        # Rounds to save space
        percent_df = np.round(percent_df, 6)
        # except:
        #     print(df.dtypes)
        #     raise Exception
        # converts NAN to None, for proper JSON encoding
        working_df = percent_df.where(pd.notnull(percent_df), None)
        # creates series of race percentages as a dictionary
        # this allows us to add percentages to the main table,
        # without adding many more columns
        dict_series = working_df.apply(pd.Series.to_dict, axis=1)
        dict_series.name = f'{metric}_percentages'
        return percent_df, dict_series

    @classmethod
    def __pd_process_race(cls):
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

        for geo_area in cls.df_dict:
            geo_df = cls.df_dict[geo_area]

            # creates df using original columns
            # prevents conflicts with new columns
            # race_values = tuple(cls.data_metrics['race'].values())
            race_values = cls.get_data_values('race')
            race_df = geo_df.loc[:, race_values]

            # divides df by race_total column to calculate percentages
            race_percent_df, pct_dict_series = cls.__nest_percentages(race_df, 'race_total')  # noqa: E501

            # creates series of majority race demographics
            majority_series = race_percent_df.apply(majority, axis=1)
            majority_series.name = 'race_majority'

            # creates df from the series for merging
            percentage_df = pd.concat([pct_dict_series,
                                       majority_series], axis=1)

            # A join would add the values as two new columns
            # Trying to merge creates the columns if they don't exist
            # and updates them if they do exist
            # Potential simplification with attribute access,
            # however I'm not confident that handles missing data, etc
            try:
                geo_df = geo_df.merge(percentage_df,
                                      left_index=True, right_index=True,
                                      suffixes=(False, False))
            except ValueError:
                geo_df.update(percentage_df)
            cls.df_dict[geo_area] = geo_df

    @classmethod
    def __pd_process_poverty(cls):
        for geo_area in cls.df_dict:
            geo_df = cls.df_dict[geo_area]

            # creates df using original columns
            # prevents conflicts with new columns
            poverty_values = cls.get_data_values('poverty')
            poverty_df = geo_df.loc[:, poverty_values]
            total_col = 'poverty_population_total'
            pct_df, pct_series = cls.__nest_percentages(poverty_df, total_col)

            q_df = pct_df.apply(np.quantile, q=(0, 0.25, 0.5, 0.75, 1))  # noqa: E501
            q_dict = q_df.to_dict(orient='list')
            cls.data_bins.update({'quantiles': q_dict})  # noqa: E501

            # create quantile bins using natural breaks algorithm.
            # bin_count could be increased to > 4 if needed.
            q_dict = calculate_natural_breaks_bins(pct_df, bin_count=4,
                                                   column_names=["poverty_population_poverty",  # noqa: E501
                                                                 "poverty_population_poverty_child"])  # noqa: E501

            cls.data_bins.update({'natural_breaks': q_dict})

            # A join would add the values as two new columns
            # Trying to merge creates the columns if they don't exist
            # and updates them if they do exist
            # Potential simplification with attribute access,
            # however I'm not confident that handles missing data, etc
            try:
                geo_df = geo_df.merge(pct_series,
                                      left_index=True, right_index=True,
                                      suffixes=(False, False))
            except ValueError:
                geo_df.update(pct_series)
            cls.df_dict[geo_area] = geo_df


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
    import requests

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
    return bin_dict
