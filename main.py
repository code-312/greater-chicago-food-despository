'''
Defines and calls Census data requests
'''
#move this function to census_response.py
from acs5racedemographics import processRaceData


d = {
    "race": {
        "var_dict":{
            'B03002_001E': 'race_total', 'B03002_005E': \
            'race_native','B03002_004E': 'race_black', 'B03002_003E':\
            'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
            'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
            'B03002_012E': 'race_hispaniclatino_total'
        },
        "table":'https://api.census.gov/data/2018/acs/acs5?',
        "function_ls" : [processRaceData]
    },
    "poverty":{
        "var_dict":{
            'S1701_C01_001E': 'poverty_population_total','S1701_C02_001E':'poverty_population_poverty'
        },
        "table":'https://api.census.gov/data/2018/acs/acs5/subject?',
        "function_ls" : []
    }
}


def main(d):
    import census_response
    d_ls = []
    for v in d.values():
        var_dict, table, function_ls = v.values()
        v_ls = census_response.getCensusData(var_dict, table, function_ls)
        d_ls += v_ls
    return d_ls

if __name__ == '__main__':
    main(d)

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
        'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
        'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
        'B03002_012E': 'race_hispaniclatino_total'
}
Calculate or pull percentages of race data?
'''