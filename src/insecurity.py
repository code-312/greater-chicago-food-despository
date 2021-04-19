import os
import sys
import json
import pandas as pd
sys.path.append(os.path.abspath(''))
# from src.census_response import CensusData  # noqa: E402


def load_merged(fp='final_jsons/df_merged_json.json'):
    with open(fp) as f:
        return json.load(f)


def save_with_insecurity(data,
                         fp='final_jsons/df_merged_with_insecurity.json'):
    with open(fp, 'w') as f:
        return json.dump(data, f)


def merge_insecurity_data():
    fp = 'final_jsons/Countyfood_insecurity_rates_12.15.2020.json'
    ins_df = pd.read_json(fp, orient='index')
    ins_df = ins_df.drop(labels='County Name', axis=1)
    ins_df.columns = ['2018', '2020_projected',
                      '2018_child', '2020_child_projected']
    print(ins_df)
    ins_dict = json.loads(ins_df.to_json(orient='index'))
    merged_data = load_merged()
    for k, v in merged_data['county_data'].items():
        v['insecurity_data'] = ins_dict[k]

    save_with_insecurity(merged_data)

if __name__ == '__main__':
    merge_insecurity_data()
