import json
from census_response import getCensusResponse
import requests

def main():
    zip_data = getRaceData('zip')
    county_data = getRaceData('county')

def getRaceData(geography):
    if geography == 'zip':
        geo = 'zip code tabulation area:*'
    elif geography == 'county':
        geo = 'county:*&in=state:17'
    else:
        raise Exception("Invalid Geography")

    #race tables (requesting specific tables faster than filtering out group)
    get_ls= ['B02001_001E', 'B02001_002E', 'B02001_003E', 'B02001_004E',\
                    'B02001_005E', 'B02001_006E', 'B02001_007E', 'B02001_008E',\
                    'B02001_009E', 'B02001_010E']
                    
    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'

    response = getCensusResponse(detailed_table, get_ls, geo)
    #race_data is list of lists, where list elements are rows
    #headers defined by group_data_variables elements
    race_data = response.json()

    
    group_response = requests.get('https://api.census.gov/data/2018/acs/acs5/groups/B02001')
    group_data_variables = group_response.json()['variables']
    
    #Labels table columns with group variable labels
    labelled_race_ls = [[]]

    for i, row in enumerate(race_data):
        #header row
        if i == 0:
            for c, col in enumerate(race_data[0]):
                #Gets variable label from group data
                if col in group_data_variables:
                    label = group_data_variables[col]['label']
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
          race_data_IL = [d[:-2] + [f"{d[-2]}{d[-1]}"] for d in labelled_race_ls[1:]]
    #Json format
    #{'geography':
        #{'metric_one': 1234,
        #'metric_two': 5678}}
        
    final_json = {}
    print(race_data_IL[:2])

    for d in race_data_IL:
        #set variables to list elements
        name, race_total, race_white, race_black, race_americanindian, \
            race_asian, race_pacific, race_other, race_twoplus_total, \
            race_twoplus_inclusive, race_twoplus_exclusive, g = d
       
        #Calculate percentages?
        
        #create geography json
        g_json = {f'name_{geography}': name, 'race_total': race_total, \
            'race_white': race_white, 'race_black': race_black, \
            'race_americanindian': race_americanindian, 'race_asian': race_asian,\
            'race_pacific': race_pacific, 'race_other': race_other,\
            'race_twoplus_total': race_twoplus_total, \
            'race_twoplus_inclusive':race_twoplus_inclusive,\
            'race_twoplus_exclusive':race_twoplus_exclusive}

        #set geography key to geography json value
        final_json[g] = g_json

    #save file
    with open(F'final_jsons/acs5{geography}race_output.json', 'w') as f:
        json.dump(final_json, f)
    
if __name__ == '__main__':
    main()