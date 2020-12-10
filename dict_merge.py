from acs5countypoverty import main as countypoverty_script
from acs5zippoverty import main as zippoverty_script
from acs5racedemographics import main as racedemo_script
import json

def main():
    #Data Dicts
    countyPovertyDict = countypoverty_script()
    zipPovertyDict = zippoverty_script()
    zipRaceDict, countyRaceDict = racedemo_script()

    #Create Geo Lists
    countyDictList = [countyPovertyDict, countyRaceDict]
    zipDictList = [zipPovertyDict, zipRaceDict]

    #Pass Geo Lists into Merge function
    mergedCountyDict = merge(countyDictList)
    mergedZipDict = merge(zipDictList)
    
    #write to json
    with open(F'final_jsons/mergedCounty_output.json', 'w') as f:
            json.dump(mergedCountyDict, f)

    with open(F'final_jsons/mergedZip_output.json', 'w') as f:
        json.dump(mergedZipDict, f)

    final_json_ls = [mergedCountyDict, mergedZipDict]
    
    return final_json_ls


def merge(dictList = list()):
    '''
    Merges county data dictionaries
    input: list of geo data dictionaries (list)
            dictionary format {'countyFIP':{'metric1':1}}
            within each dictionary assumes all counties include the same metrics
    output: merged geo data dictionary, same format
    '''
    mergedDict = dict()
    
    #Get all the geocodes in both datasets
    mergedKeys = set()
    for d in dictList:
        mergedKeys.update(set(d))
    
    #loop through all geocodes
    for k in mergedKeys:
        #creates geocode key for mergedDict
        mergedDict[k] = dict()
        for i, d in enumerate(dictList):
            #if the geocode is not in the dictionary, print to console and continue
            try:
                value = list(d[k])
            except:
                print(k, F' not in dictList[{i}]')
                continue
            for v in value:
                #if the metric is already in the dictionary it is a duplicate
                if v in mergedDict[k]:
                    #if the duplicate key includes an identical value continue
                    if mergedDict[k][v] == d[k][v]:
                        continue
                    #Otherwise, raise exception and return metric name
                    e = 'Duplicate metric key: rename to avoid overwrite'
                    raise Exception(e, v)
                #The metric is not in the dictionary, add it
                else:
                    mergedDict[k][v] = d[k][v]
    return mergedDict

if __name__ == '__main__':
    main()