from zipfile import ZipFile, ZIP_DEFLATED
import os
import json
from typing import List


def zip(fp: str) -> None:
    files = ['final_jsons/countyData.json',
             'final_jsons/zipData.json',
             'final_jsons/metaData.json']

    if check_version(fp):
        version_match(fp, files)
        return None

    try:
        os.remove(fp)
    except OSError:
        if os.path.exists(fp):
            print("Other OSError")
        pass

    with ZipFile(fp, "w", ZIP_DEFLATED) as z:
        for f in files:
            z.write(f)


def check_version(fp: str) -> bool:
    with ZipFile(fp) as z:
        meta_str = z.read('final_jsons/metaData.json')
    zip_meta = json.loads(meta_str)

    with open('final_jsons/metaData.json') as f:
        new_meta = json.load(f)

    return zip_meta['version'] == new_meta['version']


def version_match(fp: str, files: List[str]) -> None:
    # verifies file names are the same
    with ZipFile(fp) as z:
        zipls = z.namelist()
        assert set(zipls) == set(files)

    # verifies content of files
    for f in files:
        with open(f) as fo:
            new = json.load(fo)
        with ZipFile(fp) as z:
            original = json.loads(z.read(f))

        assert original == new
