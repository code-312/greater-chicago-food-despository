from api_keys import census_key
import json
import requests

def getCensusResponse(table_url,get_ls,geo):
    '''
    Returns response from census query
    input:
    
    output:
    '''
    
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={census_key}'
    response = requests.get(url)
    return(response)