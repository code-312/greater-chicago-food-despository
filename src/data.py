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

    __obj_list = [{"zip": {}}, {"county": {}}]

    def __init__(self, metric: str, df: pd.DataFrame, 
                 path: tuple = (), fp: str = None):
        # replace with read/write?
        self.parent = path[-1]
        self.name = f"{self.parent}_{metric}"
        self.metric = metric
        self.df = df
        self.fp = fp
        assert isinstance(path, tuple)
        self.path = path
        self.__post_init__()

    def __post_init__(self):
        self.dict = self.__make_dict(self.path)
        self.__obj_list.append(self.dict)
        if self.fp is None:
            self.fp = f"data_objects/{self.name}.pkl"
        self.to_pickle()
    
    def __repr__(self):
        s = f'GCFDData({self.name})'
        return s

    def to_pickle(self) -> None:
        with open(self.fp, "wb") as f:
            pickle.dump(self, f)

    def __make_dict(self, path):
        if len(path) >= 2:
            k, v = path[:2]
            n_d = self.__make_dict(path[2:])
            final = {k: {v: n_d}}
            return final
        elif path:
            # assert isinstance(path, str)
            k = path[0]
            v = self.to_dict()
            return {k: v}
        else:
            return 'BREAK'

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
                        if isinstance(d, GCFDData):
                            d = d.__make_dict(d.path)
                        cls.__obj_list.append(d)

    @classmethod
    def get_data(cls) -> dict:
        return deepcopy(cls.__obj_list)

    @classmethod
    def merge_dict(cls, d1, d2):
        '''
        Merges d2 into d1
        '''
        for k in d2:
            if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                cls.merge_dict(d1[k], d2[k])
            else:
                d1[k] = d2[k]
        return d1

    # @classmethod
    # def export_data(cls, fp: str = "final_jsons/test_data_obj.json") -> None:
    #     final_dict = {'zip': {},
    #                   'county': {}}
    #     parent_dict = {}
    #     for v in cls.get_data().values():
    #         # breakpoint()
    #         print(v)
    #         v_dict = v.to_dict()

    #         # Adds child data to parent dict
    #         # If child came before parent
    #         if v.name in parent_dict:
    #             print("No children in parent_dict")
    #             child = parent_dict[v.name]
    #             v_dict[child.name] = child.df.to_dict()

    #         # Checks for parent
    #         # MAKE RECURSIVE
    #         if v.parent in final_dict:
    #             print("Parent in final_dict")
    #             # final_dict[v.parent][v.name] = v_dict
    #             parent = final_dict[v.parent]
    #             if parent:
    #                 for k in parent:
    #                     # breakpoint()
    #                     k_dict = dict(v_dict[k].get(v.name, {}))
    #                     parent[k][v.name] = k_dict
    #             else:
    #                 parent = v_dict
    #             final_dict[v.parent] = parent
                    
    #         elif v.parent:
    #             print("Adding parent to parent_dict")
    #             parent_dict[v.parent] = v
    #         else:
    #             print("adding self to final_dict")
    #             final_dict[v.name] = v_dict
    #         print("-"*10)
    #     # breakpoint()
    #     with open(fp, "w") as f:
    #         json.dump(final_dict, f, separators=(',', ':'),
    #                   cls=NumpyEncoder)

