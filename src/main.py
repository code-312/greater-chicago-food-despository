import os
import sys
import time
sys.path.append(os.path.abspath(''))
# Raises linting error because not at top of file
# Not sure how to resolve this with the pathing
import memory_profiling.memory_profile_helpers as mph  # noqa: E402
import src.census_response  # noqa: E402
import src.wic  # noqa: E402
from src.snap import merge_snap_data  # noqa: E402
from src.child_nutrition import merge_child_nutrition_data  # noqa: E402
from src import data  # noqa: E402
from src.insecurity import get_food_insecurity_data  # noqa: E402
import src.zip_data  # noqa: E402


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
    combined_data.add(wic_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading WIC Data took: {0:.2f} seconds".format(duration))

    print("Reading Food Insecurity Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    insecurity_data: data.Wrapper = get_food_insecurity_data()
    combined_data.add(insecurity_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading Food Insecurity Data took: {0:.2f} seconds".format(duration))  # noqa: E501

    print("Reading Snap Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    snap_data = merge_snap_data([('2019', 'data_folder/snap/SNAP_2019.xlsx'), ('2020', 'data_folder/snap/SNAP_2020.xlsx')])  # noqa: E501
    combined_data.add(snap_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading Snap Data took: {0:.2f} seconds".format(duration))  # noqa: E501

    print("Reading Child Nutrition Data")
    mph.record_current_memory_usage_if_enabled()
    start_time = time.time()
    cn_data = merge_child_nutrition_data([('2019', 'data_folder/child_nutrition/child_meals_2019.xlsx')])  # noqa: E501
    combined_data.add(cn_data)
    if (verbose):
        duration = time.time() - start_time
        print("Reading Child Nutrition Data took: {0:.2f} seconds".format(duration))  # noqa: E501

    merged_data: data.Merged = data.merge(combined_data)
    # Increase version number to publish updates to final_jsons.zip
    merged_data.meta.version = '0.1.0'
    with open('final_jsons/countyData.json', "w") as f:
        f.write(data.to_json(merged_data.county_data))
    with open('final_jsons/metaData.json', "w") as f:
        f.write(data.to_json(merged_data.meta))
    with open('final_jsons/zipData.json', "w") as f:
        f.write(data.to_json(merged_data.zip_data))

    src.zip_data.zip('final_jsons/final_jsons.zip')

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
