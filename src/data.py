import pandas as pd
from dataclasses import dataclass
import pickle
import json
from numpyencoder import NumpyEncoder

'''
Defines data structure and relationships
Classes:
    DataObject

Methods:
    load_data - loads data from disk
    get_data - returns data from memory
    export_data - saves data to merged JSON
'''

gcfd_data = {}


@dataclass
class DataObject:
    name: str
    df: pd.DataFrame
    parent: str = None
    fp: str = None

    def __post_init__(self):
        if self.fp is None:
            self.fp = f"data_objects/{self.name}.pkl"
        self.to_pickle()
        gcfd_data[self.name] = self
    
    def to_pickle(self):
        with open(self.fp, "wb") as f:
            pickle.dump(self, f)
    
    def to_dict(self):
        d_dict = self.df.to_dict(orient="index")
        # json_str = json.dumps(d_dict)
        return d_dict


def load_data():
    with open("data_objects/test_zip.pkl", "rb") as f:
        d = pickle.load(f)
        gcfd_data[d.name] = d


def get_data():
    return gcfd_data.copy()


def export_data():
    final_dict = {}
    parent_dict = {}
    for v in gcfd_data.values():
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

    with open("final_jsons/test_data_obj.json", "w") as f:
        json.dump(final_dict, f, cls=NumpyEncoder)