import os
import sys

sys.path.append(os.path.abspath(''))
# Raises linting error because not at top of file
# Not sure how to resolve this with the pathing
from src import uploadJson  # noqa: E402
import src.config as config  # noqa: E402


# Taking out of commission until new geojson format requested developed
# def test_main():
#    from src import main
#    import json
#    import geojson
#     #from src import main
#     main_dict = main.main(['county'])
#     for v in main_dict.values():
#         v_str = json.dumps(v)
#         v_geojson = geojson.loads(v_str)
#         assert v_geojson.is_valid == True

def test_auth():
    db = uploadJson.auth_firebase()
    cook = db.reference('/county_data/17031').get()
    assert cook['NAME'] == 'Cook County, Illinois'


def test_secrets():
    assert type(config.CENSUS_KEY) == str
    assert type(config.FIREBASE_SERVICE_KEY) == str
    assert config.CENSUS_KEY != ''
    assert config.FIREBASE_SERVICE_KEY != ''
