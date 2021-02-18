from src.config import CENSUS_KEY
import json
import requests

def getCensusResponse(table_url,get_ls,geo):
    '''
    Concatenates url string and returns response from census api query
    input:
        table_url (str): census api table url
        get_ls (ls): list of tables to get data from
        geo (str): geographic area and filter
    output:
        response (requests.response): api response
    '''
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={CENSUS_KEY}'
    # print(f"Calling for {geo}: {get_ls}")
    response = requests.get(url)
    # print(f"{response} Received")
    return(response)

def getCensusData(table_code_dict, census_table, function_ls = [], geo_ls=["zip","county"]):

    '''
    Obtains Census data and returns zip and county dictionaries
    input:
        table_code_dict (dict):
            Key: Census Table Variable (str)
            Value: Descriptive name of variable (str)
        census_table (str, url): Census table url
        geo_ls (ls): Geographies to return, accepts "zip" and "county" as keywords
                    additional geographies may be passed, but must be valid Census API keywords
        function_ls (ls): functions to run sequentially on final_js, before saved and returned
    output:
        final_json (dict):
            key: zip or county code (str)
            value: metrics (dict)
                key: metric name (str)
                value: metric value (object)
    '''
    final_json_ls = []
    for geography in geo_ls:
        if geography == 'zip':
            geo = 'zip code tabulation area:*'
        elif geography == 'county':
            geo = 'county:*&in=state:17'
        else:
            raise Exception(f"Invalid Geography: {geography}")

        key_ls = list(table_code_dict.keys())
        value_ls = list(table_code_dict.values())
        #Values name format: topic_property_subproperty
        topic = value_ls[0].split('_')[0]
        value_ls.insert(0, 'name')
        value_ls.append('g')

        response = getCensusResponse(census_table, key_ls, geo)

        response_data = response.json()

        #Labels table columns with group variable labels
        #Add better comment
        labelled_ls = [[]]
        # print("Creating Labelled List")
        for i, row in enumerate(response_data):
            #header row
            if i == 0:
                for c, col in enumerate(response_data[0]):
                    #Gets variable label from group data
                    if col in table_code_dict:
                        label = table_code_dict[col]
                        labelled_ls[0].append(label)
                    #Variables not in group data added to list
                    else:
                        labelled_ls[0].append(col)
            #converts data strings to ints
            else:
                new_row = []
                for v, n in enumerate(row):
                    if v == 0 or v == len(row)-1:
                        new_row.append(n)
                    else:
                        try:
                            new_row.append(int(n))
                        except:
                            #Value likely null
                            new_row.append(n)

                labelled_ls.append(new_row)
        IL_data = []
        
        if "zip" == geography:
        #filter zipcodes
        #IL zipcodes begin with numbers in zip_ls_IL
            zip_ls_IL = ['60', '61', '62']

            for d in labelled_ls[1:]:
                #print(d[3][:2])
                if d[-1][:2] in zip_ls_IL:
                    IL_data.append(d)
        else:
            #creates county geo labels
            IL_data = [d[:-2] + [f"{d[-2]}{d[-1]}"] for d in labelled_ls[1:]]
        final_json = {geography:{}}

        for d in IL_data:
            
            #create geography json
            #topic_metrics nests topic data
            geo_dict = {l:d[i] for i, l in enumerate(value_ls)}
            
            g_json = {f'name_{geography}': geo_dict['name'], f'{topic}_metrics': geo_dict}

            #set geography key to geography json value
            final_json[geography][geo_dict['g']] = g_json

        for f in function_ls:
            final_json[geography] = f(final_json[geography])

        #save file
        # print("Final Json created, saving to file")
        # breakpoint()
        with open(F'final_jsons/acs5{geography}{topic}_output.json', 'w') as f:
            json.dump(final_json, f, separators=(',',':'))
        
        final_json_ls.append(final_json)
    return final_json_ls

def searchTable(table_json_ls: list, keyword_ls: list, filter_function_ls: list) -> list:
    '''
    Filters variable tables by keyword and filter
    input:
        table_json_ls (response.json() list object): list of lists from census variable table api
        keyword_ls (list):  list of keyword strings
                            keyword filter applied to the third element of the input list (concept column)
        filter_function_ls (list): list of functions that filter table_json_ls with filter method
    output:
        return_json_ls (list): list, same format as table_json_ls, filtered
    '''    
    return_json_ls = list()
    
    #runs filter for each function in filter_function_ls
    for f in filter_function_ls:
        table_json_ls = list(filter(f, table_json_ls))
    
    #adds rows with keyword(s) in concept column to return_json_ls
    for d in table_json_ls:
        try:
            for k in keyword_ls:
                #d[2] is the concept column, d[1] is the label column
                if k.lower() in d[2].lower() or k.lower() in d[1].lower():
                    continue
                else:
                    break
            else:
                return_json_ls.append(d)
        except: 
            continue
    
    return return_json_ls

def county_fips(reverse = False) -> dict:
    '''
    Requests county fips from census API and returns list of IL county FIPS
    input: reverse (bool) reverses keys and values in output
    output: il_json (dict) {'county name': 'fip'}
    '''
    import requests

    url = 'https://api.census.gov/data/2010/dec/sf1?get=NAME&for=county:*'

    response = requests.get(url)

    #filter for IL
    il_county = lambda x: x[1] == '17'

    response_json = response.json()

    if reverse:
        il_json = {county[1]+county[2]: county[0]  for county in response_json if il_county(county)}
    else:
        il_json = {county[0]: county[1]+county[2] for county in response_json if il_county(county)}

    return il_json

def processRaceData(data_json):
    '''
    Determines majority race and race percentages from getRaceData final json and adds to race_metrics
    input:
        data_json (dict): final_json from getRaceData
    output:
        data_json (dict): input with 'race_majority' and 'percentages' metrics added to 'race_metrics'
    '''
    #Majority filter function
    majority = lambda x, y: x/y >= 0.5

    for d in data_json.items():
        #race_majority default value, since another majority would overwrite
        race_majority = "majority_minority"
        race_data = d[1]['race_metrics']
        race_total = race_data['race_total']
        percentages = {}
        #if: checks that total is not zero
        if race_total:
            for k, v in race_data.items():
                #skips evaluating race_total, 'name' and 'g'
                try:
                    skip_ls = ['race_total','name','g']
                    if k in skip_ls:
                        continue
                    elif majority(v,race_total):
                        race_majority = k
                    #Add percentage
                    race_pct = v/race_total * 100
                    percentages[k] = race_pct
                except Exception as e:
                    print(e) #error
                    print(d) #current data object
                    print(race_data) #racemetrics
                    print(v, race_total) #race data value, race_total metric
                    raise Exception('Error')
        #Add majority and percentages to json
        data_json[d[0]]['race_metrics']['race_majority'] = race_majority
        data_json[d[0]]['race_metrics']['percentages'] = percentages
        #For dev investigation if printed
        if race_majority == 'race_other' or race_majority == 'race_twoplus_exclusive':
            print(d)
    
    return data_json
