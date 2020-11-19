from api_keys import census_key
import json
import requests

#Estimate!!Total!!Population for whom poverty status is determined
pop_table = 'S1701_C01_001E'
#Estimate!!Below poverty level!!Population for whom poverty status is determined
poverty_table = 'S1701_C02_001E'

subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'
get = f'NAME,{pop_table},{poverty_table}'
#county level request for IL (state 17)
geo = 'county:*&in=state:17'
url = f'{subject_table}get={get}&for={geo}&key={census_key}'
response = requests.get(url)

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
    #create county json
    county_json = {'name_county':name, 'population_total': pop_total_int, 'population_poverty': pop_poverty_int, 'percent_poverty': pct_poverty}
    #set county key to county json value
    final_json[fip_final] = county_json


#save file
with open('final_jsons/acs5countypoverty_output.json', 'w') as f:
    json.dump(final_json, f)



