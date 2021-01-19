from census_response import getCensusResponse
import json

def main():
    #Estimate!!Total!!Population for whom poverty status is determined
    pop_table = 'S1701_C01_001E'
    #Estimate!!Below poverty level!!Population for whom poverty status is determined!!AGE!!Under 18 years
    child_poverty_table = 'S1701_C02_002E'
    
    #If additional subdivision are needed
    #'S1701_C02_003E' = AGE!!Under 18 years!! Under 5 years!!
    #'S1701_C02_004E' = AGE!!Under 18 years!! 5 to 17 years!!

    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'
    get_ls = [pop_table, child_poverty_table]
    #county level request for IL (state 17)
    geo = 'county:*&in=state:17'

    response = getCensusResponse(subject_table, get_ls, geo)

    #poverty_data is list of lists, where list elements are rows
    #header row: name, population total, population poverty, fip state, fip county
    poverty_data = response.json()

    #Json format
    #{'countyfip': (countyfip = concatenation state and county fip numbers)
        #{'metric_one': 1234,
        #'metric_two': 5678}}
        
    final_json = {}

    for d in poverty_data[1:]:
        #set variables to list elements
        name, pop_total_str, pop_poverty_str, fip_state, fip_county = d
        #convert strings to ints
        pop_total_int = int(pop_total_str)
        pop_poverty_int = int(pop_poverty_str)
        #concat strings
        fip_final = fip_state + fip_county
        #calculate percent poverty
        pct_poverty = pop_poverty_int / pop_total_int * 100
        #create county child json
        county_child_json = {'name_county':name, 'population_total': pop_total_int, 'population_poverty': pop_poverty_int, 'percent_poverty': pct_poverty}
        #set county key to county child json value
        final_json[fip_final] = county_child_json

    #save file
    with open('final_jsons/acs5county_child_poverty_output.json', 'w') as f:
        json.dump(final_json, f)
    
    return final_json

if __name__ == '__main__':
    main()

