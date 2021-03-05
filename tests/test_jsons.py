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


def test_requirements():
    import pkg_resources

    requirements_path = "requirements.txt"
    with open(requirements_path) as f:
        requirements = pkg_resources.parse_requirements(f)
        for r in requirements:
            r = str(r)
            pkg_resources.require(r)
            # breakpoint()


def test_auth():
    # TODO determine why this fails on github
    db = uploadJson.auth_firebase()
    cook = db.reference('/countyData/17031').get()
    assert cook['name_county'] == 'Cook County, Illinois'


def test_secrets():
    assert type(config.CENSUS_KEY) == str
    assert type(config.FIREBASE_SERVICE_KEY) == str
    assert config.CENSUS_KEY != ''
    assert config.FIREBASE_SERVICE_KEY != ''
