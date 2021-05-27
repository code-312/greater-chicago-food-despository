import requests
from typing import Any
import json
import urllib


def query_census_api(street_addr: str, zip: str) -> Any:
    p = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress'
    benchmark = 'Public_AR_Current'
    vintage = 'Current_Current'
    addr_encoded = urllib.parse.quote_plus('{} {}'.format(street_addr, zip))
    args = '?address={}&benchmark={}&vintage={}&format=json'.format(
        addr_encoded, benchmark, vintage)
    result = requests.get('{}{}'.format(p, args))
    if result.status_code != 200:
        raise Exception(result.text)
    return json.loads(result.text)


# given the input
#  '1060 W Addison St', '60613'
# will return the tuple
#  ('17031', 'Cook')
def address_to_county(street_addr: str, zip: str) -> tuple:
    raw_result = query_census_api(street_addr, zip)
    matches = raw_result['result']['addressMatches']
    if len(matches) == 0:
        return (None, None)
    counties = matches[0]['geographies']['Counties']
    if len(counties) == 0:
        return (None, None)
    county = counties[0]
    return (county['GEOID'], county['BASENAME'])
