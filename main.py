'''
Defines and calls Census data requests
'''
def censusData():
    '''
    Defines class CensusData
    CensusData instances created
    Loops through CensusData instances calling getData method to produce dictionaries
    Returns list of dictionaries
    '''
    from census_response import getCensusData, processRaceData

    class CensusData:
        #set tracks instances of the class
        class_set = set()
        def __init__(self, var_dict:dict, table:str, function_ls:list = [], geo_ls:list =["zip","county"]):
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
    #Values name format: topic_property_subproperty...
    race_dict = {'B03002_001E': 'race_total', 'B03002_005E': \
                'race_native','B03002_004E': 'race_black', 'B03002_003E':\
                'race_white', 'B03002_009E': 'race_twoplus_total', 'B03002_007E': 'race_pacific', \
                'B03002_008E':'race_other', 'B03002_006E': 'race_asian',\
                'B03002_012E': 'race_hispaniclatino_total'}
    race_functions = [processRaceData]
    #variable does not need to be defined, but it is for readability
    race = CensusData(race_dict, detailed_table, race_functions)

    #define poverty instance
    poverty_dict = {'S1701_C01_001E': 'poverty_population_total','S1701_C02_001E':'poverty_population_poverty',\
                    'S1701_C02_002E': 'poverty_population_poverty_child'}
                    #If additional subdivision are needed
                    #'S1701_C02_003E' = AGE!!Under 18 years!! Under 5 years!!
                    #'S1701_C02_004E' = AGE!!Under 18 years!! 5 to 17 years!!
    poverty = CensusData(poverty_dict, subject_table)

    #reference class set
    class_set = CensusData.class_set
    
    d_ls = []
    
    for c in class_set:
        d_ls += c.getData()

    return d_ls

def main():
    '''
    Calls censusData function to create CensusData instances and return list of dictionaries
    Calls dict_merge to merge list of dictionaries by geo_area and save jsons to file
    '''
    import dict_merge
    d_ls = censusData()
    d_merged_dict = dict_merge.main(d_ls)
    
    return d_merged_dict


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