import json
import geojson
import os
import sys
sys.path.append(os.path.abspath(''))  
from src import main
from src import uploadJson

def test_main():
    #from src import main
    main_dict = main.main(['county'])
    
    for v in main_dict.values():
        v_str = json.dumps(v)
        v_geojson = geojson.loads(v_str)
        assert v_geojson.is_valid == True


def test_requirements():
    import pkg_resources

    requirements_path = "requirements.txt"
    with open(requirements_path) as f:
        requirements = pkg_resources.parse_requirements(f)
        for r in requirements:
            r = str(r)
            require = pkg_resources.require(r)
            # breakpoint()

def test_auth():
    #TODO determine why this fails on github
    db = uploadJson.authFirebase()
    cook = db.reference('/countyData/17031').get()
    assert cook['name_county'] == 'Cook County, Illinois'

def test_secrets():
    import src.config as config
    assert type(config.CENSUS_KEY) == str
    assert type(config.FIREBASE_SERVICE_KEY) == str
    