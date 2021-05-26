import src.main
import os

def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)

def test_run():
    delete_file('final_jsons/df_dump.json')
    delete_file('final_jsons/df_merged_json.json')
    src.main.main()
    assert os.path.exists('final_jsons/df_dump.json')
    assert os.path.exists('final_jsons/df_merged_json.json')
