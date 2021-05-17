import os
import sys
import time
sys.path.append(os.path.abspath(''))
# Raises linting error because not at top of file
# Not sure how to resolve this with the pathing
import memory_profiling.memory_profile_helpers as mph  # noqa: E402
import src.census_response  # noqa: E402
from src.file_to_json import file_to_wrapper  # noqa: E402
import src.wic  # noqa: E402
from src import data


def main(geo_ls=["zip", "county"], verbose: bool = False) -> None:
    '''
    Gathers data from different sources, combines them into
    one data structure and then writes it to file in two formats
    '''
    mph.setup_memory_usage_file_if_enabled()

    print("Reading Census Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    combined_data: data.Wrapper = src.census_response.download_census_data()
    if (verbose):
        duration = time.time() - start_time
        print("Reading Census Data took: {0:.2f} seconds".format(duration))  # noqa: E501

    print("Reading WIC Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    wic_data: data.Wrapper = src.wic.read_wic_data()
    combined_data: data.Wrapper = data.combine(combined_data, wic_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading WIC Data took: {0:.2f} seconds".format(duration))

    print("Reading Food Insecurity Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    insecurity_data: data.Wrapper = file_to_wrapper('data_folder', blacklist=['Key'])
    combined_data: data.Wrapper = data.combine(combined_data, insecurity_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading Food Insecurity Data took: {0:.2f} seconds".format(duration))  # noqa: E501

    with open('final_jsons/df_dump.json', "w") as f:
        f.write(data.to_json(combined_data))

    merged_data: data.Merged = data.merge(combined_data)
    with open('final_jsons/df_merged_json.json', "w") as f:
        f.write(data.to_json(merged_data))

    mph.record_current_memory_usage_if_enabled()
    mph.generate_report_if_enabled()

    return None


if __name__ == '__main__':
    main()

'''
Race data notes
----------------------
determine whether to remove unused variables

All Variables:
"var_dict":{
        'B03002_021E': 'race_hispaniclatino_twoplus_exclusive',\
        'B03002_020E': 'race_hispaniclatino_twoplus_inclusive',\
        'B03002_001E': 'race_total', 'B03002_005E': \
        'race_native','B03002_004E': 'race_black', 'B03002_003E':\
        'race_white', 'B03002_002E': 'race_total_not_hispaniclatino',\
        'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
        'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
        'B03002_013E': 'race_hispaniclatino_white',\
        'B03002_012E': 'race_hispaniclatino_total', 'B03002_011E':\
        'race_twoplus_exclusive', 'B03002_010E': 'race_twoplus_inclusive',\
        'B03002_017E': 'race_hispaniclatino_pacific', 'B03002_016E': \
        'race_hispaniclatino_asian', 'B03002_015E': \
        'race_hispaniclatino_native',
        'B03002_014E': 'race_hispaniclatino_black',\
        'B03002_018E': 'race_hispaniclatino_other', \
        'B03002_019E': 'race_hispaniclatino_twoplus_total'
}
Used Variables for Race
"var_dict":{
        'B03002_001E': 'race_total', 'B03002_005E': \
        'race_native','B03002_004E': 'race_black', 'B03002_003E':\
        'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E':
        'race_pacific', \
        'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
        'B03002_012E': 'race_hispaniclatino_total'
}
Calculate or pull percentages of race data?
'''
