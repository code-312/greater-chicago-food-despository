from dotenv import load_dotenv
import os

load_dotenv()


def test_requirements():
    import pkg_resources

    requirements_path = "requirements.txt"
    with open(requirements_path) as f:
        requirements = pkg_resources.parse_requirements(f)
        for r in requirements:
            r = str(r)
            try:
                pkg_resources.require(r)
            except Exception as e:
                print(e)
                print("Conflict in " + r)
                assert False


def test_environment():
    CENSUS_KEY = os.getenv("CENSUS_KEY")  # noqa: N806
    assert(type(CENSUS_KEY) == str)
