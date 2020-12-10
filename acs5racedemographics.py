import json
from census_response import getCensusResponse
import requests

def main():
    zip_data = getRaceData('zip')
    county_data = getRaceData('county')

    return [zip_data, county_data]

def getRaceData(geography):
    '''
    Calls census api for race demographic data by specified geography
    input:
        geography (str): "zip" or "county"
    output:
        final_json (dict):
            key: zip or county code (str)
            value: metrics (dict)
                key: metric name (str)
                value: metric value (object)
    '''
    if geography == 'zip':
        geo = 'zip code tabulation area:*'
    elif geography == 'county':
        geo = 'county:*&in=state:17'
    else:
        raise Exception("Invalid Geography")

    #Variable List: https://api.census.gov/data/2018/acs/acs5/groups/B02001.html
    #race tables (requesting specific tables faster than filtering out group)
    var_dict = {'B03002_021E': 'race_hispaniclatino_twoplus_exclusive',\
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
                'B03002_019E': 'race_hispaniclatino_twoplus_total'}

    race_ls = list(var_dict.keys())
    value_ls = list(var_dict.values())
                    
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'

    response = getCensusResponse(detailed_table, race_ls, geo)
    
    #race_data is list of lists, where list elements are rows
    #headers defined by group_data_variables elements
    race_data = response.json()
    
    #Labels table columns with group variable labels
    labelled_race_ls = [[]]

    for i, row in enumerate(race_data):
        #header row
        if i == 0:
            for c, col in enumerate(race_data[0]):
                #Gets variable label from group data
                if col in var_dict:
                    label = var_dict[col]
                    labelled_race_ls[0].append(label)
                #Variables not in group data added to list
                else:
                    labelled_race_ls[0].append(col)
        #converts data strings to ints
        else:
            new_row = []
            for v, n in enumerate(row):
                if v == 0 or v == len(row)-1:
                    new_row.append(n)
                else:
                    new_row.append(int(n))

            labelled_race_ls.append(new_row)

    race_data_IL = []
    
    if "zip" == geography:
        #filter zipcodes
        #IL zipcodes begin with numbers in zip_ls_IL
        zip_ls_IL = ['60', '61', '62']

        for d in labelled_race_ls[1:]:
            #print(d[3][:2])
            if d[-1][:2] in zip_ls_IL:
                race_data_IL.append(d)
    else:
        #creates county geo labels
        race_data_IL = [d[:-2] + [f"{d[-2]}{d[-1]}"] for d in labelled_race_ls[1:]]
            
    #Json format
    #{'geography':
        #{'metric_one': 1234,
        #'metric_two': 5678}}
        
    final_json = {}

    for d in race_data_IL:
        #set variables to list elements
        #determine whether to pull unused variables
        name, race_hispaniclatino_twoplus_exclusive, \
        race_hispaniclatino_twoplus_inclusive, race_total, race_native, race_black,\
        race_white, race_total_not_hispaniclatino, race_twoplus_total, race_pacific,\
        race_other, race_asian, race_hispaniclatino_white, race_hispaniclatino_total,\
        race_twoplus_exclusive, race_twoplus_inclusive, race_hispaniclatino_pacific,\
        race_hispaniclatino_asian, race_hispaniclatino_native, \
        race_hispaniclatino_black, race_hispaniclatino_other, \
        race_hispaniclatino_twoplus_total, g = d
       
        #Calculate percentages?
        
        #create geography json
        #race_metrics nests racial data
        race_dict = {'race_total': race_total, \
            'race_white': race_white, 'race_black': race_black, \
            'race_hispaniclatino_total' : race_hispaniclatino_total, \
            'race_native': race_native, 'race_asian': race_asian,\
            'race_pacific': race_pacific, 'race_other': race_other,\
            'race_twoplus_total': race_twoplus_total}
        
        g_json = {f'name_{geography}': name, 'race_metrics': race_dict}

        #set geography key to geography json value
        final_json[g] = g_json

    final_json = processRaceData(final_json)

    #save file
    with open(F'final_jsons/acs5{geography}race_output.json', 'w') as f:
        json.dump(final_json, f)
    
    return final_json

def processRaceData(data_json):
    '''
    Determines majority race from getRaceData final json and adds to race_metrics
    input:
        data_json (dict): final_json from getRaceData
    output:
        data_json (dict): input with 'race_majority' metric added to 'race_metrics'
    '''
    #Majority filter function
    majority = lambda x, y: x/y >= 0.5

    for d in data_json.items():
        #race_majority default value, since another majority would overwrite
        race_majority = "majority_minority"
        race_data = d[1]['race_metrics']
        race_total = race_data['race_total']
        #if checks that total is not zero
        if race_total:
            for k, v in race_data.items():
                #skips evaluating race_total
                try:
                    if k == 'race_total':
                        continue
                    elif majority(v,race_total):
                        race_majority = k
                        break
                    else:
                        continue
                except Exception as e:
                    print(e)
                    print(d)
                    print(race_data)
                    print(v, race_total)
                    raise Exception('Error')
        data_json[d[0]]['race_metrics']['race_majority'] = race_majority
        if race_majority == 'race_other' or race_majority == 'race_twoplus_exclusive':
            print(d)
    
    return data_json

if __name__ == '__main__':
    main()