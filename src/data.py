import pandas as pd
import pickle
import json
from copy import deepcopy
import os
from typing import Dict, List, Any, Union

'''
Defines data structure and relationships
Classes:
    DataObject

Methods:
    load_data - loads data from disk
    get_data - returns data from memory
    export_data - saves data to merged JSON
'''


class MetaData:
    def __init__(self):
        self.data_metrics: Dict[str, Dict[str, str]] = {}  # e.g. { "race": {"B03002_001E": "race_total"} } # noqa: E501
        self.data_bins: Dict[str, Dict[str, List[float]]] = {}  # e.g. { "quantiles": { "poverty_population_poverty": [1, 2, 3] } } # noqa: E501


class Wrapper:
    def __init__(self):
        self.meta = MetaData()
        self.county: Dict[str, Dict[str, Any]] = {}  # e.g. { "NAME": { "17001": "Adams County, Illinois" } } # noqa: E501
        self.zip: Dict[str, Dict[str, Any]] = {}  # e.g. { "race_total": { "60002": 24066 } } # noqa: E501

class Merged:
    def __init__(self):
        self.meta = MetaData()
        self.county_data: Dict[str, Dict[str, Any]] = {}  # e.g. { "17001": { "NAME": "Adams County, Illinois" } } # noqa: E501
        self.zip_data: Dict[str, Dict[str, Any]] = {}  # e.g. { "60002": { "race_total": 24066 } } # noqa: E501

def combine_inner_dictionaries(dict_1: Dict[str, Dict], dict_2: Dict[str, Dict]) -> Dict[str, Dict]:
    combined_dict = {}
    combined_dict.update(dict_1)

    for key in dict_2:
        if key in combined_dict:
            combined_dict[key].update(dict_2[key])
        else:
            combined_dict[key] = dict_2[key]
    return combined_dict


def combine(data_1: Wrapper, data_2: Wrapper) -> Wrapper:

    combined_data = Wrapper()
    combined_data.zip.update(data_1.zip)
    combined_data.zip.update(data_2.zip)
    combined_data.county.update(data_1.county)
    combined_data.county.update(data_2.county)
    combined_data.meta.data_metrics.update(data_1.meta.data_metrics)
    combined_data.meta.data_metrics.update(data_2.meta.data_metrics)
    combined_data.meta.data_bins = combine_inner_dictionaries(data_1.meta.data_bins, data_2.meta.data_bins)

    return combined_data


def to_json(data: Union[Wrapper,Merged], pretty_print: bool = False) -> str:
    if pretty_print:
        indent = 4
    else:
        indent = None
    return json.dumps(data, sort_keys=True, indent=indent, default=lambda o: o.__dict__)


def from_county_dataframe(df: pd.DataFrame) -> Wrapper:
    wrapper = Wrapper()
    wrapper.county = df.to_dict()
    return wrapper


def from_zip_dataframe(df: pd.DataFrame) -> Wrapper:
    wrapper = Wrapper()
    wrapper.zip = df.to_dict()
    return wrapper


def merge_internal(input: Dict, output: Dict) -> None:
    for metric in input.keys():

        metric_group_name = metric.split("_")[0] + "_data"

        for geo_area_id in input[metric]:
            if geo_area_id not in output:
                output[geo_area_id] = {}

            if metric_group_name not in output[geo_area_id]:
                output[geo_area_id][metric_group_name] = {}

            output[geo_area_id][metric_group_name][metric] = deepcopy(input[metric][geo_area_id])


def merge(wrapper: Wrapper) -> Merged:
    merged_data = Merged()
    merged_data.meta.data_bins.update(wrapper.meta.data_bins)
    merged_data.meta.data_metrics.update(wrapper.meta.data_metrics)

    merge_internal(wrapper.county, merged_data.county_data)
    merge_internal(wrapper.zip, merged_data.zip_data)

    return merged_data
