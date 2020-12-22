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