import aiohttp
import asyncio
import async_timeout
import os
from typing import Dict, Union, List

from client.us_census_variable_names import (
    TOTAL_HOUSEHOLDS_RECEIVING_FOOD_STAMPS_IN_LAST_YEAR, 
    ILLINOIS_STATE_CODE
)

async def get_request(session: aiohttp.ClientSession, url: str, params: Dict[str, str]) -> Union[List, Dict]:
    async with async_timeout.timeout(10):
        async with session.get(url, params=params) as response:
            return await response.json()

async def get_total_households_receiving_food_stamps_per_county(api_key: str) -> List[List[str]]:
    async with aiohttp.ClientSession() as session:
        year = "2019"
        params = {
            'get': f'NAME,{TOTAL_HOUSEHOLDS_RECEIVING_FOOD_STAMPS_IN_LAST_YEAR}',
            'for': 'county:*',
            'in': f'state:{ILLINOIS_STATE_CODE}',
            'key': api_key
            }
        response = await get_request(session, f'https://api.census.gov/data/{year}/acs/acs1', params)
        return response
