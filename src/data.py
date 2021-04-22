import pandas as pd
import pickle
import json
from numpyencoder import NumpyEncoder
from copy import deepcopy

'''
Defines data structure and relationships
Classes:
    DataObject

Methods:
    load_data - loads data from disk
    get_data - returns data from memory
    export_data - saves data to merged JSON
'''


class GCFDData:
    obj_dict: dict = {}

    def __init__(self, name: str, df: pd.DataFrame, 
                 parent: str = None, fp: str = None):
        # replace with read/write?
        self.name = name
        self.df = df
        self.parent = parent
        self.fp = fp
        self.__post_init__()

    def __post_init__(self):
        if self.fp is None:
            self.fp = f"data_objects/{self.name}.pkl"
        self.to_pickle()
        self.obj_dict[self.name] = self
    
    def to_pickle(self) -> None:
        with open(self.fp, "wb") as f:
            pickle.dump(self, f)
    
    def to_dict(self) -> dict:
        d_dict = self.df.to_dict(orient="index")
        # json_str = json.dumps(d_dict)
        return d_dict

    @classmethod
    def load_data(cls, fp: str = "data_objects/test_zip.pkl") -> None:
        with open(fp, "rb") as f:
            d = pickle.load(f)
            cls.obj_dict[d.name] = d

    @classmethod
    def get_data(cls) -> dict:
        return deepcopy(cls.obj_dict)
    
    @classmethod
    def clear_data(cls) -> None:
        cls.obj_dict = {}

    @classmethod
    def export_data(cls, fp: str = "final_jsons/test_data_obj.json") -> None:
        final_dict = {}
        parent_dict = {}
        for v in cls.obj_dict.values():
            v_dict = v.to_dict()

            # Adds child data to parent dict
            # If child came before parent
            if v.name in parent_dict:
                child = parent_dict[v.name]
                v_dict[child.name] = child.df.to_dict()

            # Checks for parent
            if v.parent in final_dict:
                # final_dict[v.parent][v.name] = v_dict
                parent = final_dict[v.parent]
                for k in parent:
                    # breakpoint()
                    parent[k][v.name] = dict(v_dict[k][v.name])
                    
            elif v.parent:
                parent_dict[v.parent] = v
            else:
                final_dict[v.name] = v_dict

        with open(fp, "w") as f:
            json.dump(final_dict, f, separators=(',', ':'),
                      cls=NumpyEncoder)

