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