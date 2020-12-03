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
    response = requests.get(url)
    return(response)

def searchTable(table_json_ls: list, keyword_ls: list, filter_function_ls=list()):
    assert (type(table_json_ls)==type(keyword_ls)==type(filter_function_ls)==list), "searchTable Parameters must be lists"
    return_json = list()
    
    for f in filter_function_ls:
        table_json_ls = list(filter(f, table_json_ls))
    #print(table_json_ls)
    for d in table_json_ls:
        try:
            for k in keyword_ls:
                if k.lower() in d[2].lower():
                    continue
                else:
                    break
            else:
                return_json.append(d)
        except: 
            continue
    
    return return_json