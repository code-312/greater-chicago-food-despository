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
        # Separators option here minimizes whitespace
        json.dump(data, dst_file, separators=(',', ':'))


def merge_ins_data(insecurity_src: str,
                   merged_src: str, merged_dst: str) -> None:
    ins_df = pd.read_json(insecurity_src, orient='index')

    # Remove County Name column because it already exists in merged_src
    ins_df.drop(labels='County Name', axis=1, inplace=True)

    # Rename columns to stay consistent with merged_src formatting
    ins_df.columns = ['2018', '2020_projected',
                      '2018_child', '2020_child_projected']

    # This is a little roundabout way of doing things,
    # but it preserves the FIPS code as a string,
    # and avoids some floating-point rounding issues
    # that cropped up doing a straight df.to_dict()
    ins_dict = json.loads(ins_df.to_json(orient='index'))
    merged_data = load_merged(merged_src)

    # merged_dst should be shaped like this:
    # {
    #     meta:{ ... }
    #     zip_data: {...}
    #     county_data: {
    #         <fips>: {
    #             race_data:{...}
    #             poverty_data:{...}
    #             insecurity_data:{...}
    #             NAME:{...}
    #         }
    #     }
    # }

    for fips, county_data in merged_data['county_data'].items():
        county_data['insecurity_data'] = ins_dict[fips]

    save_merged(merged_data, merged_dst)
