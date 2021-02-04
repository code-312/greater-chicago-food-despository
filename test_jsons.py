import json
import geojson

def test_main():
    import main
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