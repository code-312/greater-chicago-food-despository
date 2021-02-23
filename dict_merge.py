import json
import memory_profiling.memory_profile_helpers as mph


def main(d_ls):
    '''
    Puts zip and county data into separate lists
    Sends data to merge() and writes to merged json
    Returns jsons in list
    
    input:
        d_ls (list): list of dictionaries
            dictionary format:
            {geo_area:{geo_code:{metrics...},...}}
    output:
        final_json_ls (list): list of dictionaries
            len() = 2 (default, county and zip)
    '''
    # unpack d_ls into dictionary by geo_area
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
    # calls merge function on each geo_area
    for k, v in d_dict.items():
        geo_json = {}
        geo_json[k] = merge(v)
        final_json_ls.append(geo_json)
        # breakpoint()
        with open(F'final_jsons/merged{k}_output.json', 'w') as f:
            json.dump(geo_json, f)
            mph.record_current_memory_usage_if_enabled()

    # saves merged_dict to file
    with open(F'final_jsons/merged_output.json', 'w') as f:
        merged_dict = {**final_json_ls[0], **final_json_ls[1]}
        # breakpoint()
        json.dump(merged_dict, f)


        # print(inspect.stack())
        mph.record_current_memory_usage_if_enabled()

    return final_json_ls


def merge(dictList=list()):
    '''
    Merges data dictionaries
    input: list of geo data dictionaries (list)
            dictionary format {geo_area:{'geo_code':{'metric1':1,...},...}}
            within each dictionary assumes all geo-areas include the same metrics
    output: merged geo data dictionary, same format
    '''
    # TODO What happens if some geo areas do not have all the data elements?
    # Error handled: prints geo area not in list index
    # Do we want to add the missing data with null values?
    # breakpoint()
    mergedDict = dict()

    # Get all the geocodes in both datasets
    mergedKeys = set()
    for d in dictList:
        # breakpoint()
        mergedKeys.update(set(d.keys()))

    # loop through all geocodes
    for k in mergedKeys:
        # creates geocode key for mergedDict
        mergedDict[k] = dict()
        for i, d in enumerate(dictList):
            # breakpoint()
            # if the geocode is not in the dictionary, print to console and continue
            # TODO add missing geocode metric here?
            try:
                value = list(d[k])
            except:
                print(k, F' not in dictList[{i}]')
                continue
            for v in value:
                # if the metric is already in the dictionary it is a duplicate
                if v in mergedDict[k]:
                    # if the duplicate key includes an identical value continue
                    if mergedDict[k][v] == d[k][v]:
                        continue
                    # Otherwise, raise exception and return metric name
                    e = 'Duplicate metric key: rename to avoid overwrite'
                    raise Exception(e, v)
                # The metric is not in the dictionary, add it
                else:
                    mergedDict[k][v] = d[k][v]
    return mergedDict


if __name__ == '__main__':
    main()
