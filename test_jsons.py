from json.decoder import JSONDecodeError
import json

def test_main():
    from main import main
    main()
    check_file('final_jsons/merged_output.json')

def test_requirements():
    import pkg_resources

    requirements_path = "requirements.txt"
    with open(requirements_path) as f:
        requirements = pkg_resources.parse_requirements(f)
        for r in requirements:
            r = str(r)
            require = pkg_resources.require(r)
            # breakpoint()

def check_file(fp):
    #read in json
    #Invalid JSON (non-string keys) raises JSONDecodeError
    try:
        with open(fp) as f:
            data = json.load(f)
    except JSONDecodeError as j:
        print(j)
        print("Keys must be strings")
        print("If using python to create JSON, use JSON library to dump dictionary to JSON file")
        return j
    except Exception as e:
        print(e)
        return e

    #Primary key must contain dictionary
    #TODO determine if second-level dictionary must be dictionary
    for d in data:
        #test the value, should be dictionary
        v = data[d]
        assert(type(v)==dict)
