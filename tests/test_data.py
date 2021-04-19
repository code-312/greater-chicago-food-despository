'''
Test/Demo for data implementation

Read in DF, create DataObjects, tests export
'''
import os
import sys

# Module Not Found Error without this code
sys.path.append(os.path.abspath(''))

import pandas as pd  # noqa: E402
import src.data as GCFDData  # noqa: E402


def read_data():
    if GCFDData.get_data() != {}:
        GCFDData.gcfd_data = {}
    base = pd.read_pickle('./tests/resources/data_60002_base.xz')
    pct = pd.read_pickle('./tests/resources/data_60002_pct.xz')
    GCFDData.DataObject('zip', base, fp="./tests/resources/base_obj.pkl")
    GCFDData.DataObject('poverty_percentages', pct,
                        parent='zip', fp='./tests/resources/pct_obj.pkl')


def test_pickle_output():
    read_data()
    data_copy_zip = GCFDData.get_data()['zip']
    GCFDData.gcfd_data = {}
    assert GCFDData.get_data() == {}
    GCFDData.load_data("./tests/resources/base_obj.pkl")
    data_new_zip = GCFDData.get_data()['zip']
    assert type(data_copy_zip) == type(data_new_zip)
    assert data_copy_zip.to_dict() == data_new_zip.to_dict()


def test_export_output():
    read_data()
    fp = './tests/resources/test_data_class_new.json'
    GCFDData.export_data(fp)
    with open('./tests/resources/test_data_class_main.json') as main:
        with open(fp) as f:
            assert main.read() == f.read()
