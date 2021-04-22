from src.config import CENSUS_KEY
import jenkspy
import json
import requests
import numpy as np
import pandas as pd
from numpyencoder import NumpyEncoder
from typing import Dict, List
from src.data import DataObject


def get_census_response(table_url, get_ls, geo):
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

def census_df():
    '''
    Creates the DF from census response
    '''
    df = pd.DataFrame()

    return df

def census_data_object():
    '''
    returns the census data object
    calls Census DF
    '''

    pass