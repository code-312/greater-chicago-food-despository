import pandas as pd
import pickle
import json
from numpyencoder import NumpyEncoder
from copy import deepcopy
import os
from typing import Dict, List

'''
Defines data structure and relationships
Classes:
    DataObject

Methods:
    load_data - loads data from disk
    get_data - returns data from memory
    export_data - saves data to merged JSON
'''


def collect_data() -> None:
    '''
    Top level function 
    '''
    pass


class GCFDData:
    '''
    Goal:
        Add parent/child nodes
    Current:
        Init:
            Adds self to parent list
                If no parent, raises error
        Unpacks percentages, but doesn't unpack metrics into zip.
        Doesn't save meta to file
    '''
    __meta_dict = {
        "bins": {
            "quantiles": {},
            "natural_breaks": {}
        }
    }

    __obj_dict = {"zip": list(), "county": list()}

    def __init__(self, metric: str, df: pd.DataFrame, 
                 parent: str = None, fp: str = None):
        # replace with read/write?
        self.name = f"{parent}_{metric}"
        self.metric = metric
        self.df = df
        self.fp = fp
        self.parent = parent
        self.__post_init__()

    def __post_init__(self):
        self.__set_parent()
        if self.fp is None:
            self.fp = f"data_objects/{self.name}.pkl"
        self.to_pickle()
        try:
            self.__obj_dict[self.name] = list()
        except TypeError:
            print(self)
    
    def __repr__(self):
        s = f'GCFDData({self.name})'
        return s
    
    def __set_parent(self):
        # Why don't I just pass self?
        try:
            p_ls = self.__obj_dict[self.parent]
            p_ls.append(self)
            # breakpoint()
        except TypeError:
            print(self)

    def get_path(self):
        s = [self.parent, self.name]
        s.insert(0, self.parent.get_path())
        return s

    def to_pickle(self) -> None:
        with open(self.fp, "wb") as f:
            pickle.dump(self, f)
        with open('data_objects/obj_dict.pkl', 'wb') as f:
            pickle.dump(self.__obj_dict, f)
    
    def to_dict(self) -> dict:
        d_dict = self.df.to_dict(orient="index")
        # json_str = json.dumps(d_dict)
        return d_dict


    @classmethod
    def write_meta(cls, meta_dict: dict):
        cls.__meta_dict.update(meta_dict)
        return cls.__meta_dict
        

    @classmethod
    def load_data(cls, dir: str = "data_objects/") -> None:
        for _, _, files in os.walk(dir):
            for fp in files:
                with open(dir+fp, "rb") as f:
                    try:
                        d = pickle.load(f)
                    except AttributeError:
                        print(fp)
                        continue
                    else:
                        if fp == 'obj_dict.pkl':
                            cls.__obj_dict = d

    @classmethod
    def get_data(cls) -> dict:
        return deepcopy(cls.__obj_dict)
    
    @classmethod
    def clear_data(cls) -> None:
        cls.__obj_dict = {}

    @classmethod
    def export_data(cls, fp: str = "final_jsons/test_data_obj.json") -> None:
        final_dict = {'zip': {},
                      'county': {}}
        parent_dict = {}
        for v in cls.get_data().values():
            # breakpoint()
            print(v)
            v_dict = v.to_dict()

            # Adds child data to parent dict
            # If child came before parent
            if v.name in parent_dict:
                print("No children in parent_dict")
                child = parent_dict[v.name]
                v_dict[child.name] = child.df.to_dict()

            # Checks for parent
            # MAKE RECURSIVE
            if v.parent in final_dict:
                print("Parent in final_dict")
                # final_dict[v.parent][v.name] = v_dict
                parent = final_dict[v.parent]
                if parent:
                    for k in parent:
                        # breakpoint()
                        k_dict = dict(v_dict[k].get(v.name, {}))
                        parent[k][v.name] = k_dict
                else:
                    parent = v_dict
                final_dict[v.parent] = parent
                    
            elif v.parent:
                print("Adding parent to parent_dict")
                parent_dict[v.parent] = v
            else:
                print("adding self to final_dict")
                final_dict[v.name] = v_dict
            print("-"*10)
        # breakpoint()
        with open(fp, "w") as f:
            json.dump(final_dict, f, separators=(',', ':'),
                      cls=NumpyEncoder)

def merge_dict(dict1, dict2, name):
    # print(dict1.keys())
    # print(dict2.keys())
    new_dict = {}
    for d in dict2:
        for geo_code in dict1:
            
            dict1[geo_code][d] = dict2[d].get(geo_code, {})
            new_dict[geo_code] = {}
            new_dict[geo_code][name] = dict1[geo_code]
    return new_dict

def key_merge(dict1, dict2):
    new_dict = {}
    i = 0
    j = 0
    for geo, value in dict1.items():
        i += 1
        zip_dict = value
        for k, v in dict2[geo].items():
            j += 1
            zip_dict[k] = v
        else:
            new_dict[geo] = zip_dict
            # breakpoint()
            if '17067' in zip_dict:
                print('zip')
                # breakpoint()
            elif '17067' in new_dict:
                print('new')  # HERE
                # breakpoint()
    # print(i, j)
    # second call, fucks it
    # breakpoint()
    return new_dict

def unpack_data(parent_list):
    data_dict = {}
    for d in parent_list:
        child_ls = data.get(d.name)
        # print("d.name: ", d.name)
        # print("Memo: ", memo)
        # print('-'*10)
        if child_ls:
            child_dict = unpack_data(child_ls)
            self_dict = d.to_dict()
            merged_dict = merge_dict(self_dict, child_dict, d.metric)
            # breakpoint()
            data_dict[d.name] = merged_dict
        else:
            print(d.name)
            # if d.name == "county_race_percentages":
                # breakpoint()
            data_dict[d.name] = d.to_dict()
        memo.add(d.name)
    else:
        final_dict = {}
        breakpoint()
        for k, v in data_dict.items():
            if final_dict == {}:
                final_dict = v
                # breakpoint()
                continue
            # breakpoint()
            final_dict = key_merge(v, final_dict)
    # print(data_dict)
    # breakpoint()
    # final_dict = data_dict
    return final_dict

#remake export dat
data = GCFDData.get_data()
final_dict = {}
memo = set()
# for k, v in data.items():

for k in ["zip", "county"]:
    v = data[k]
    print("k: ", k)
    if k not in memo:
        final_dict[k]=unpack_data(v)