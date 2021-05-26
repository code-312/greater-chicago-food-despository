import src.main
import os

def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)  # remove() raises an exception if the file doesn't exist

def test_run():
    delete_file('final_jsons/countyData.json')
    delete_file('final_jsons/metaData.json')
    delete_file('final_jsons/zipData.json')
    src.main.main()
    assert os.path.exists('final_jsons/countyData.json')
    assert os.path.exists('final_jsons/metaData.json')
    assert os.path.exists('final_jsons/zipData.json')
