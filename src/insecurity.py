import os
import sys
import json
import pandas as pd
sys.path.append(os.path.abspath(''))


def load_merged(src_path: str):
    with open(src_path) as src_file:
        return json.load(src_file)


def save_merged(data, dst_path: str) -> None:
    with open(dst_path, 'w') as dst_file:
        json.dump(data, dst_file)


def merge_ins_data(insecurity_src: str, merged_src: str, merged_dst: str) -> None:
    ins_df = pd.read_json(insecurity_src, orient='index')
    ins_df.drop(labels='County Name', axis=1, inplace=True)
    ins_df.columns = ['2018', '2020_projected',
                      '2018_child', '2020_child_projected']
    ins_dict = json.loads(ins_df.to_json(orient='index'))
    merged_data = load_merged(merged_src)
    for k, v in merged_data['county_data'].items():
        v['insecurity_data'] = ins_dict[k]

    save_merged(merged_data, merged_dst)
