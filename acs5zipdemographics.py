import json
from census_response import getCensusResponse
import requests

def main():
    #race group table
    get_ls = ['group(B02001)']

    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'

    #zip level request 
    #Unable to filter request by state
    geo = 'zip code tabulation area:*'

    response = getCensusResponse(detailed_table, get_ls, geo)

    #race_data is list of lists, where list elements are rows
    #headers defined by group_data_variables elements
    race_data = response.json()
    
    group_response = requests.get('https://api.census.gov/data/2018/acs/acs5/groups/B02001')
    group_data_variables = group_response.json()['variables']
    
    #Keep columns with estimates, filtering out margin of error and annotations
    #Labels table columns with group variable labels
    filtered_race_ls = [[],[]]
    #filters out margin and annotations
    filter_ls = ['Margin', 'Annota']

    for i, row in enumerate(race_data):
        #header row
        if i == 0:
            for c, col in enumerate(race_data[0]):
                #Gets variable label from group data
                if col in group_data_variables:
                    if group_data_variables[col]['label'][:6] not in filter_ls:
                        label = group_data_variables[col]['label']
                        filtered_race_ls[0].append(c)
                        filtered_race_ls[1].append(label)
                    else:
                        continue
                #Variables not in group data added to list
                else:
                    filtered_race_ls[0].append(c)
                    filtered_race_ls[1].append(col)
        #filtered rows
        else:
            new_row = []
            for n in filtered_race_ls[0]:
                elem = race_data[i][n]
                #Convert data strings to int
                if n in filtered_race_ls[0][2:-2]:
                    new_row.append(int(elem))
                else:
                    new_row.append(elem)
            filtered_race_ls.append(new_row)


    #filter zipcodes
    #IL zipcodes begin with numbers in zip_ls_IL
    zip_ls_IL = ['60', '61', '62']

    race_data_IL = []

    for d in filtered_race_ls[1:]:
        #print(d[3][:2])
        if d[-1][:2] in zip_ls_IL:
            race_data_IL.append(d)
            
    #Json format
    #{'zipcode:
        #{'metric_one': 1234,
        #'metric_two': 5678}}
        
    final_json = {}

    for d in race_data_IL:
        #set variables to list elements
        name, geo_id, race_total, race_white, race_black, race_americanindian, \
            race_asian, race_pacific, race_other, race_twoplus_total, \
            race_twoplus_inclusive, race_twoplus_exclusive, name2, zipcode = d
        #Calculate percentages?
        
        #create zip json
        zip_json = {'name_zip': name, 'race_total': race_total, \
            'race_white': race_white, 'race_black': race_black, \
            'race_americanindian': race_americanindian, 'race_asian': race_asian,\
            'race_pacific': race_pacific, 'race_other': race_other,\
            'race_twoplus_total': race_twoplus_total, \
            'race_twoplus_inclusive':race_twoplus_inclusive,\
            'race_twoplus_exclusive':race_twoplus_exclusive}
        #set zip key to zip json value
        final_json[zipcode] = zip_json

    #save file
    with open('final_jsons/acs5ziprace_output.json', 'w') as f:
        json.dump(final_json, f)

if __name__ == '__main__':
    main()