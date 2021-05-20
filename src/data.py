import pandas as pd
import json
import numpy
import jenkspy
from copy import deepcopy
from typing import Dict, List, Any, Union, Optional


class MetaData:
    def __init__(self):
        self.data_metrics: Dict[str, Dict[str, str]] = {}  # e.g. { "race": {"B03002_001E": "race_total"} } # noqa: E501
        self.data_bins: Dict[str, Dict[str, List[float]]] = {}  # e.g. { "quantiles": { "poverty_population_poverty": [1, 2, 3] } } # noqa: E501


class Wrapper:
    def __init__(self):
        self.meta = MetaData()
        self.county: Dict[str, Dict[str, Any]] = {}  # e.g. { "NAME": { "17001": "Adams County, Illinois" } } # noqa: E501
        self.zip: Dict[str, Dict[str, Any]] = {}  # e.g. { "race_total": { "60002": 24066 } } # noqa: E501

    def add(self, other) -> None:
        self.zip.update(other.zip)
        self.county.update(other.county)
        self.meta.data_metrics.update(other.meta.data_metrics)
        self.meta.data_bins = combine_inner_dictionaries(self.meta.data_bins, other.meta.data_bins)  # noqa: E501


class Merged:
    def __init__(self):
        self.meta = MetaData()
        self.county_data: Dict[str, Dict[str, Any]] = {}  # e.g. { "17001": { "NAME": "Adams County, Illinois" } } # noqa: E501
        self.zip_data: Dict[str, Dict[str, Any]] = {}  # e.g. { "60002": { "race_total": 24066 } } # noqa: E501


def combine_inner_dictionaries(dict_1: Dict[str, Dict], dict_2: Dict[str, Dict]) -> Dict[str, Dict]:  # noqa: E501
    combined_dict = {}
    combined_dict.update(dict_1)

    for key in dict_2:
        if key in combined_dict:
            combined_dict[key].update(dict_2[key])
        else:
            combined_dict[key] = dict_2[key]
    return combined_dict


def json_encoder(object: Any) -> Any:
    if isinstance(object, numpy.int64):
        return int(object)
    else:
        return object.__dict__  # serialize objects as dictionaries


def to_json(data: Union[Wrapper, Merged], pretty_print: bool = False) -> str:
    if pretty_print:
        indent: Optional[int] = 4
        separators = None
    else:
        indent = None
        separators = (',', ':')
    return json.dumps(data,
                      sort_keys=True,  # make the output deterministic
                      indent=indent,  # turn on or off new lines and indents
                      separators=separators,  # turn on or off trimming whitespace  # noqa: E501
                      default=json_encoder)


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

        metric_group = metric.split("_")[0]

        if metric_group == "race" or \
           metric_group == "poverty" or \
           metric_group == "insecurity":

            metric_group_name = metric_group + "_data"

            for geo_area_id in input[metric]:
                if geo_area_id not in output:
                    output[geo_area_id] = {}

                if metric_group_name not in output[geo_area_id]:
                    output[geo_area_id][metric_group_name] = {}

                output[geo_area_id][metric_group_name][metric] = deepcopy(input[metric][geo_area_id])  # noqa: E501
        else:
            for geo_area_id in input[metric]:
                if geo_area_id not in output:
                    output[geo_area_id] = {}

                output[geo_area_id][metric] = deepcopy(input[metric][geo_area_id])  # noqa: E501


def merge(wrapper: Wrapper) -> Merged:
    merged_data = Merged()
    merged_data.meta.data_bins.update(wrapper.meta.data_bins)
    merged_data.meta.data_metrics.update(wrapper.meta.data_metrics)

    merge_internal(wrapper.county, merged_data.county_data)
    merge_internal(wrapper.zip, merged_data.zip_data)

    return merged_data


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
        natural_breaks = jenkspy.jenks_breaks(column_data, nb_class=bin_count)
        # round for space and avoid floating point imprecision
        bin_dict[cn] = list(numpy.round(natural_breaks, 6))
    return bin_dict
