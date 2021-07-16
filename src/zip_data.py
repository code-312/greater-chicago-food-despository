from zipfile import ZipFile, ZIP_DEFLATED
import os


def zip(fp: str) -> None:
    try:
        os.remove(fp)
    except OSError:
        if os.path.exists(fp):
            print("Other OSError")
        pass

    with ZipFile(fp, "w", ZIP_DEFLATED) as z:
        z.write('final_jsons/countyData.json')
        z.write('final_jsons/zipData.json')
        z.write('final_jsons/metaData.json')
