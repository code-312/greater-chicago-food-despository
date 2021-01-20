from json.decoder import JSONDecodeError
# from acs5countypoverty import main as countypoverty_script
# from acs5zippoverty import main as zippoverty_script
# from acs5racedemographics import main as racedemo_script
import json

# def test_county_poverty():
#     #runs county script to create/update county json
#     countypoverty_script()
#     #tests county json file
#     check_file('final_jsons/acs5countypoverty_output.json')

# def test_zip_poverty():
#     #runs zip script to create/update zip json
#     zippoverty_script()
#     #tests zip json file
#     check_file('final_jsons/acs5zippoverty_output.json')


# def test_race_demographics():
#     #runs zip script to create/update zip json
#     racedemo_script()
#     #tests zip json file
#     check_file('final_jsons/acs5ziprace_output.json')
#     check_file('final_jsons/acs5countyrace_output.json')

def test_main():
    from main import main
    main()
    check_file('final_jsons/merged_output.json')

def check_file(fp):
    #read in json
    #Invalid JSON (non-string keys) raises JSONDecodeError
    try:
        with open(fp) as f:
            data = json.load(f)
    except JSONDecodeError as j:
        print(j)
        print("Keys must be strings")
        print("If using python to create JSON, use JSON library to dump dictionary to JSON file")
        return j
    except Exception as e:
        print(e)
        return e

    #Primary key must contain dictionary
    #TODO determine if second-level dictionary must be dictionary
    for d in data:
        #test the value, should be dictionary
        v = data[d]
        assert(type(v)==dict)
