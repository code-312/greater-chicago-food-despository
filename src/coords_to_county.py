import requests
from typing import Any
import json


def query_fcc_api(lat: float, long: float) -> Any:
    path = 'https://geo.fcc.gov/api/census/block/find'
    args = '?latitude={}&longitude={}&format=json'.format(lat, long)
    result = requests.get('{}{}'.format(path, args))
    if result.status_code != 200:
        err_response = json.loads(result.text)
        raise Exception(err_response['statusMessage'])
    return json.loads(result.text)


# given the input
#  41.94859796974284, -87.65531124426796
# will return the tuple
#  ('17031', 'Cook')
def coords_to_county(lat: float, long: float) -> tuple:
    raw_result = query_fcc_api(lat, long)
    county = raw_result['County']
    return (county['FIPS'], county['name'])
