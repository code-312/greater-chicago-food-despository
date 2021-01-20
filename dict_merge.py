<<<<<<< HEAD
import json

def main(d_ls):
    '''
    Puts zip and county data into separate lists
    Merges data and writes to merged json
    Returns jsons in list
    '''
    #unpack d_ls
    d_dict = {}
    for d in d_ls:
        d_keys = str(list(d.keys())[0])
        d_values = list(d.values())[0]
        if d_keys not in d_dict:
            d_dict[d_keys] = [d_values]
        else:
            d_dict[d_keys].append(d_values)

    final_json_ls = []
    # breakpoint()
    for k,v in d_dict.items():
        geo_json = {}
        geo_json[k] = merge(v)
        final_json_ls.append(geo_json)
        # breakpoint()
        with open(F'final_jsons/merged{k}_output.json','w') as f:
            json.dump(geo_json, f)
    
    with open(F'final_jsons/merged_output.json','w') as f:
        merged_dict = {**final_json_ls[0], **final_json_ls[1]}
        # breakpoint()
        json.dump(merged_dict, f)

=======
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
    
>>>>>>> 250623b9afaadccb3f1f173f837f491e50764b2b
    return final_json_ls


def merge(dictList = list()):
    '''
<<<<<<< HEAD
    Merges data dictionaries
    input: list of geo data dictionaries (list)
            dictionary format {'countyFIP':{'metric1':1}}
            within each dictionary assumes all geo-areas include the same metrics
    output: merged geo data dictionary, same format
    '''
    #TODO What happens if some geo areas do not have all the data elements?
    #Error handled: prints geo area not in list index
    #Do we want to add the missing data with null values?
    # breakpoint()
=======
    Merges county data dictionaries
    input: list of geo data dictionaries (list)
            dictionary format {'countyFIP':{'metric1':1}}
            within each dictionary assumes all counties include the same metrics
    output: merged geo data dictionary, same format
    '''
    #What happens if some geo areas do not have all the data elements?

>>>>>>> 250623b9afaadccb3f1f173f837f491e50764b2b
    mergedDict = dict()
    
    #Get all the geocodes in both datasets
    mergedKeys = set()
    for d in dictList:
<<<<<<< HEAD
        # breakpoint()
        mergedKeys.update(set(d.keys()))
=======
        mergedKeys.update(set(d))
>>>>>>> 250623b9afaadccb3f1f173f837f491e50764b2b
    
    #loop through all geocodes
    for k in mergedKeys:
        #creates geocode key for mergedDict
        mergedDict[k] = dict()
        for i, d in enumerate(dictList):
<<<<<<< HEAD
            # breakpoint()
            #if the geocode is not in the dictionary, print to console and continue
            #TODO add missing geocode metric here?
=======
            #if the geocode is not in the dictionary, print to console and continue
>>>>>>> 250623b9afaadccb3f1f173f837f491e50764b2b
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