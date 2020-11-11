import aiohttp
import asyncio
import async_timeout
import os

from client.us_census_client import get_total_households_receiving_food_stamps_per_county

def test_get_total_households_receiving_food_stamps_per_county():
    # Get an API key for the US Census API
    # Then run 
    #     export US_CENSUS_API_KEY="your key"
    api_key = os.environ['US_CENSUS_API_KEY']
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_total_households_receiving_food_stamps_per_county(api_key))
    assert(result[0] == ["NAME","B22001_002E","state","county"])