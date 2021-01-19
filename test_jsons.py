from acs5countypoverty import main as countypoverty_script
from acs5zippoverty import main as zippoverty_script
from acs5countypoverty_child import main as county_child_poverty_script
from acs5zippoverty_child import main as zip_child_poverty_script
from acs5racedemographics import main as racedemo_script
import json

def test_county_poverty():
    #runs county script to create/update county json
    countypoverty_script()
    #tests county json file
    check_file('final_jsons/acs5countypoverty_output.json')

def test_zip_poverty():
    #runs zip script to create/update zip json
    zippoverty_script()
    #tests zip json file
    check_file('final_jsons/acs5zippoverty_output.json')

def test_county_child_poverty():
    #runs county script to create/update county json
    county_child_poverty_script()
    #tests county json file
    check_file('final_jsons/acs5county_child_poverty_output.json')
    
def test_zip_child_poverty():
    #runs county script to create/update county json
    zip_child_poverty_script()
    #tests county json file
    check_file('final_jsons/acs5zip_child_poverty_output.json')    

def test_race_demographics():
    #runs zip script to create/update zip json
    racedemo_script()
    #tests zip json file
    check_file('final_jsons/acs5ziprace_output.json')
    check_file('final_jsons/acs5countyrace_output.json')

def check_file(fp):
    #read in json
    with open(fp) as f:
        data = json.load(f)
    
    #tests elements in data
    for d in data:
        #key should be a string
        assert(type(d)==str)

        #test the value, should be dictionary
        v = data[d]
        assert(type(v)==dict)