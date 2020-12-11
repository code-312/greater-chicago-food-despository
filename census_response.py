from api_keys import census_key
import json
import requests



def getCensusResponse(table_url,get_ls,geo):
    '''

        table_url (str): census api table url
        get_ls (ls): list of tables to get data from
        geo (str): geographic area and filter
    output:
        response (requests.response): api response
    '''
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={census_key}'
    response = requests.get(url)
    return(response)