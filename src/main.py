import os
import sys
sys.path.append(os.path.abspath(''))
# Raises linting error because not at top of file
# Not sure how to resolve this with the pathing
import memory_profiling.memory_profile_helpers as mph  # noqa: E402
from src.census_response import CensusData  # noqa: E402

'''
Defines and calls Census data requests
'''


def census_data(geo_ls=["zip", "county"]):
    '''
    Defines class CensusData
    CensusData instances created
    Loops through CensusData instances \
    calling getData method to produce dictionaries
    Returns list of dictionaries
    '''
    # Census tables
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'
    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

    # define race instance
    # Values name format: topic_property_subproperty...
    # B03002_003E: Does not include people of hispanic/latino origin
    race_metrics = ('race',
                    {'B03002_001E': 'race_total', 'B03002_005E': 'race_native',
                     'B03002_004E': 'race_black', 'B03002_003E': 'race_white',
                     'B03002_009E': 'race_twoplus_total',
                     'B03002_007E': 'race_pacific',
                     'B03002_008E': 'race_other', 'B03002_006E': 'race_asian',
                     'B03002_012E': 'race_hispaniclatino_total'})
    # race_functions = [processRaceData]
    # variable does not need to be defined, but it is for readability
    race = CensusData(race_metrics, detailed_table, geo_ls)

    # define poverty instance
    poverty_metrics = ('poverty',
                       {'S1701_C01_001E': 'poverty_population_total',
                        'S1701_C02_001E': 'poverty_population_poverty',
                        'S1701_C02_002E': 'poverty_population_poverty_child'})
    # If additional subdivision are needed
    # 'S1701_C02_003E' = AGE!!Under 18 years!! Under 5 years!!
    # 'S1701_C02_004E' = AGE!!Under 18 years!! 5 to 17 years!!
    # poverty_functions = [processPovertyData]
    poverty = CensusData(poverty_metrics, subject_table, geo_ls)

    mph.record_current_memory_usage_if_enabled()
    race.get_data()
    mph.record_current_memory_usage_if_enabled()
    poverty.get_data()
    mph.record_current_memory_usage_if_enabled()
    fp = CensusData.df_to_json(zip_df=False)
    print(F"Data saved at {fp}")
    # Record heap size.

    return None


def main(geo_ls=["zip", "county"]):
    '''
    Calls censusData function to create CensusData instances
    and return list of dictionaries
    Calls dict_merge to merge list of dictionaries by geo_area
    and save jsons to file
    '''
    # from src import dict_merge
    mph.setup_memory_usage_file_if_enabled()
    mph.record_current_memory_usage_if_enabled()
    census_data(geo_ls)
    mph.record_current_memory_usage_if_enabled()

    CensusData.process_data(save=True)
    # d_merged_dict = dict_merge.main(d_ls)
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
