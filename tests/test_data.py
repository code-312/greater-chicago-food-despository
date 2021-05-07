'''
Test/Demo for data implementation

Read in DF, create DataObjects, tests export
'''
import os
import sys

# Module Not Found Error without this code
sys.path.append(os.path.abspath(''))

import pandas as pd  # noqa: E402
from src import data  # noqa: E402


# def read_data():
#     assert GCFDData.get_data() == {}
#     base = pd.read_pickle('./tests/resources/data_60002_base.xz')
#     pct = pd.read_pickle('./tests/resources/data_60002_pct.xz')
#     GCFDData('zip', base, fp="./tests/resources/base_obj.pkl")
#     GCFDData('poverty_percentages', pct,
#              parent='zip', fp='./tests/resources/pct_obj.pkl')
#     return GCFDData


# def test_pickle_output():
#     read_data()
#     data_copy_zip = GCFDData.get_data()['zip']
#     GCFDData.clear_data()
#     assert GCFDData.get_data() == {}
#     GCFDData.load_data("./tests/resources/base_obj.pkl")
#     data_new_zip = GCFDData.get_data()['zip']
#     assert type(data_copy_zip) == type(data_new_zip)
#     assert data_copy_zip.to_dict() == data_new_zip.to_dict()
#     GCFDData.clear_data()


# def test_export_output():
#     read_data()
#     fp = './tests/resources/test_data_class_new.json'
#     GCFDData.export_data(fp)
#     with open('./tests/resources/test_data_class_main.json') as main:
#         with open(fp) as f:
#             assert main.read() == f.read()
#     GCFDData.clear_data()

def test_combine():
    race_data = data.Wrapper()
    race_data.zip = { "race_total": { "60002": 24066 } }
    race_data.county = { "race_total": { "17001": 66427 } }
    race_data.meta.data_metrics = {"race": { "B03002_001E": "race_total" } }
    race_data.meta.data_bins = {"quantiles": { "race_total": [0.1, 0.2, 0.3, 0.4, 0.5] } }

    poverty_data = data.Wrapper()
    poverty_data.zip = { "poverty_population_total": { "60002": 24014 } }
    poverty_data.county = { "poverty_population_total": { "17001": 64844 } }
    poverty_data.meta.data_metrics = {"poverty": { "S1701_C01_001E": "poverty_population_total" } }
    race_data.meta.data_bins = {"natural_breaks": { "poverty_population_total": [0.6, 0.7, 0.8, 0.9, 0.11] } }

    combined_data = data.combine(race_data, poverty_data)
    assert combined_data.zip["race_total"]["60002"] == 24066
    assert combined_data.zip["poverty_population_total"]["60002"] == 24014
    assert combined_data.county["race_total"]["17001"] == 66427
    assert combined_data.county["poverty_population_total"]["17001"] == 64844
    assert combined_data.meta.data_metrics["race"]["B03002_001E"] == "race_total"
    assert combined_data.meta.data_metrics["poverty"]["S1701_C01_001E"] == "poverty_population_total"
    assert combined_data.meta.data_bins["quantiles"]["race_total"] == [0.1, 0.2, 0.3, 0.4, 0.5]
    assert combined_data.meta.data_bins["natural_breaks"]["poverty_population_total"] == [0.6, 0.7, 0.8, 0.9, 0.11]
