'''
Defines and calls Census data requests
'''

def dict_approach():
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
    return d


def class_approach():
    '''
    Advantage to class approach is function ls, default parameter(s) set by default
    Once implemented, attached function can update data for the class
    '''
    #move this function to census_response.py
    from acs5racedemographics import processRaceData
    class CensusData:
        def __init__(self, var_dict, table, function_ls=[]):
            self.var_dict = var_dict
            self.table = table
            self.function_ls = function_ls

    #define race instance
    race_dict = {'B03002_001E': 'race_total', 'B03002_005E': \
                'race_native','B03002_004E': 'race_black', 'B03002_003E':\
                'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
                'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
                'B03002_012E': 'race_hispaniclatino_total'}
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'
    race_functions = [processRaceData]
    race = CensusData(race_dict, detailed_table, race_functions)

    #define poverty instance
    poverty_dict = {'S1701_C01_001E': 'poverty_population_total','S1701_C02_001E':'poverty_population_poverty'}
    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'
    poverty = CensusData(poverty_dict, subject_table)

    #add instances to list
    class_ls = [race, poverty]
    return {i:c for i, c in enumerate(class_ls)}

def main(d):
    import census_response
    d_ls = []
    for v in d.values():
        try:
            var_dict, table, function_ls = v.values()
        except:
            var_dict = v.var_dict
            table = v.table
            function_ls = v.function_ls
        v_ls = census_response.getCensusData(var_dict, table, function_ls)
        d_ls += v_ls
    return d_ls

if __name__ == '__main__':
    d = dict_approach()
    d = class_approach()
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