from acs5countypoverty import main as countypoverty_script
import json

def main():
    #runs county script to creates/updates county json
    countypoverty_script()
    testFile('final_jsons/acs5countypoverty_output.json')


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