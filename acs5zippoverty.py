import json
from census_response import getCensusResponse

#Estimate!!Total!!Population for whom poverty status is determined
pop_table = 'S1701_C01_001E'
#Estimate!!Below poverty level!!Population for whom poverty status is determined
poverty_table = 'S1701_C02_001E'
get_ls = [pop_table, poverty_table]

subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

#zip level request 
#Unable to filter request by state
geo = 'zip code tabulation area:*'

response = getCensusResponse(subject_table, get_ls, geo)

print(response.url)
response.text

#poverty_data is list of lists, where list elements are rows
#header row: name, population total, population poverty, fip state, fip county
poverty_data = response.json()
poverty_data[:5]

#filter zipcodes
#IL zipcodes begin with numbers in zip_ls_IL
zip_ls_IL = ['60', '61', '62']

poverty_data_IL = []

for d in poverty_data[1:]:
    #print(d[3][:2])
    if d[3][:2] in zip_ls_IL:
        poverty_data_IL.append(d)
        
poverty_data_IL[:5]

#Json format
#{'countyfip': (countyfip = concatenation state and county fip numbers)
    #{'metric_one': 1234,
    #'metric_two': 5678}}
    
final_json = {}

for d in poverty_data_IL:
    #set variables to list elements
    name, pop_total_str, pop_poverty_str, zipcode = d
    #convert strings to ints
    pop_total_int = int(pop_total_str)
    pop_poverty_int = int(pop_poverty_str)
    #calculate percent poverty
    if pop_total_int != 0:
        pct_poverty = pop_poverty_int / pop_total_int * 100
    else:
        pct_poverty = 'Undefined'
    #create zip json
    zip_json = {'name_zip': name, 'population_total': pop_total_int, 'population_poverty': pop_poverty_int, 'percent_poverty': pct_poverty}
    #set county key to county json value
    final_json[zipcode] = zip_json

#save file
with open('final_jsons/acs5zippoverty_output.json', 'w') as f:
    json.dump(final_json, f)

