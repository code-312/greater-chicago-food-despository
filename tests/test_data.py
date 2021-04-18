'''
Test/Demo for data implementation

Read in DF, create DataObjects, tests export
'''
import pandas as pd
import src.data as GCFDData


def read_data():
    assert GCFDData.get_data() == {}
    base = pd.read_pickle('./resources/data_60002_base.xz')
    pct = pd.read_pickle('./resources/data_60002_pct.xz')
    GCFDData.DataObject('zip', base, fp="./resources/base_obj.pkl")
    GCFDData.DataObject('poverty_percentages', pct, 'zip', fp='./resources/pct_obj.pkl')
    diff_func()

def diff_func():
    k = GCFDData.get_data.keys()
    print(k)