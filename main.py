'''
Defines and calls Census data requests
'''

def dict_approach():
    #move this function to census_response.py
    from acs5racedemographics import processRaceData
    import census_response

    #Census tables
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'
    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

    d = {
        "race": {
            "var_dict":{
                'B03002_001E': 'race_total', 'B03002_005E': \
                'race_native','B03002_004E': 'race_black', 'B03002_003E':\
                'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
                'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
                'B03002_012E': 'race_hispaniclatino_total'
            },
            "table":detailed_table,
            "function_ls" : [processRaceData]
        },
        "poverty":{
            "var_dict":{
                'S1701_C01_001E': 'poverty_population_total','S1701_C02_001E':'poverty_population_poverty'
            },
            "table":subject_table,
            "function_ls" : []
        }
    }

    d_ls = []

    for v in d.values():
        var_dict, table, function_ls = v.values()
        v_ls = census_response.getCensusData(var_dict, table, function_ls)
        d_ls += v_ls
    
    return d_ls


'''
Advantage to class approach is function ls, default parameter(s) set by default
Once implemented, attached function can update data for the class
'''
def class_approach():
    #move this function to census_response.py
    from acs5racedemographics import processRaceData
    from census_response import getCensusData

    class CensusData:
        #set tracks instances of the class
        class_set = set()
        def __init__(self, var_dict, table, function_ls=[], geo_ls=["zip","county"]):
            self.var_dict = var_dict
            self.table = table
            self.function_ls = function_ls
            self.geo_ls = geo_ls
            self.class_set.add(self)
        
        def getData(self):
            c_ls = getCensusData(self.var_dict, self.table, self.function_ls, self.geo_ls)
            return c_ls
    
    #Census tables
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'
    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'
    
    #define race instance
    race_dict = {'B03002_001E': 'race_total', 'B03002_005E': \
                'race_native','B03002_004E': 'race_black', 'B03002_003E':\
                'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
                'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
                'B03002_012E': 'race_hispaniclatino_total'}
    race_functions = [processRaceData]
    #variable does not need to be defined, but it is for readability
    race = CensusData(race_dict, detailed_table, race_functions)

    #define poverty instance
    poverty_dict = {'S1701_C01_001E': 'poverty_population_total','S1701_C02_001E':'poverty_population_poverty'}
    poverty = CensusData(poverty_dict, subject_table)

    #reference class set
    class_set = CensusData.class_set
    
    d_ls = []
    
    for c in class_set:
        d_ls += c.getData()

    return d_ls

def main():
    import dict_merge
    d_ls = class_approach()
    d_merged_ls = dict_merge.main(d_ls)
    # breakpoint()
    #dict_approach()



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
        'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
        'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
        'B03002_012E': 'race_hispaniclatino_total'
}
Calculate or pull percentages of race data?
'''