from acs5countypoverty import main as countypoverty_script
#import acs5countypoverty.main as countypoverty_script

from acs5zippoverty import main as zippoverty_script
import json

def main():
    #runs county script to create/update county json
    countypoverty_script()
    #tests county json file
    testFile('final_jsons/acs5countypoverty_output.json')

    #runs zip script to create/update zip json
    zippoverty_script()
    #tests zip json file
    testFile('final_jsons/acs5zippoverty_output.json')


def testFile(fp):
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

if __name__ == '__main__':
    main()