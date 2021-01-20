from api_keys import CENSUS_KEY
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
    #verifies parameters are lists
    assert (type(table_json_ls)==type(keyword_ls)==type(filter_function_ls)==list), "searchTable Parameters must be lists"
    
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
        # print("Labelled List Created")
        IL_data = []
        
        # print("Filtering zipcodes")
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
        # print("Zip codes filtered")
        final_json = {}

        # print("Creating final json")
        for d in IL_data:
            
            #create geography json
            #topic_metrics nests topic data
            geo_dict = {l:d[i] for i, l in enumerate(value_ls)}
            
            g_json = {f'name_{geography}': geo_dict['name'], f'{topic}_metrics': geo_dict}

            #set geography key to geography json value
            final_json[geo_dict['g']] = g_json

        for f in function_ls:
            final_json = f(final_json)

        #save file
        # print("Final Json created, saving to file")
        with open(F'final_jsons/z_acs5{geography}new{topic}_output.json', 'w') as f:
            json.dump(final_json, f)
        
        final_json_ls.append(final_json)
    return final_json_ls