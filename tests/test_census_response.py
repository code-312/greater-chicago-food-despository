from src.census_response import CensusRequest, get_and_save_census_data


def assert_file_contents_equal(path_a: str, path_b: str):
    with open(path_a) as file_a:
        with open(path_b) as file_b:
            assert file_a.read() == file_b.read()


def test_race_dump():
    geo_ls = ["zip", "county"]

    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'

    race_metrics = {'B03002_001E': 'race_total',
                    'B03002_005E': 'race_native'}
    race = CensusRequest('race', detailed_table, race_metrics)

    actual_output_path = "tests/output/census_race_dump_actual_output.json"
    get_and_save_census_data([race], dump_output_path=actual_output_path, geo_ls=geo_ls, pretty_print=True)  # noqa: E501

    assert_file_contents_equal(actual_output_path, "tests/resources/census_race_dump_expected_output.json")  # noqa: E501


def test_race_merged():
    geo_ls = ["zip", "county"]

    detailed_table = 'https://api.census.gov/data/2018/acs/acs5?'

    race_metrics = {'B03002_001E': 'race_total',
                    'B03002_005E': 'race_native'}
    race = CensusRequest('race', detailed_table, race_metrics)

    actual_output_path = "tests/output/census_race_merged_actual_output.json"
    get_and_save_census_data([race], merged_output_path=actual_output_path, geo_ls=geo_ls, pretty_print=True)  # noqa: E501

    assert_file_contents_equal(actual_output_path, "tests/resources/census_race_merged_expected_output.json")  # noqa: E501


def test_poverty_dump():
    geo_ls = ["zip", "county"]

    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

    poverty_metrics = {'S1701_C01_001E': 'poverty_population_total',
                       'S1701_C02_001E': 'poverty_population_poverty',
                       'S1701_C02_002E': 'poverty_population_poverty_child'}
    poverty = CensusRequest('poverty', subject_table, poverty_metrics)

    actual_output_path = "tests/output/census_poverty_dump_actual_output.json"
    get_and_save_census_data([poverty], dump_output_path=actual_output_path, geo_ls=geo_ls, pretty_print=True)  # noqa: E501

    assert_file_contents_equal(actual_output_path, "tests/resources/census_poverty_dump_expected_output.json")  # noqa: E501


def test_poverty_merged():
    geo_ls = ["zip", "county"]

    subject_table = 'https://api.census.gov/data/2018/acs/acs5/subject?'

    poverty_metrics = {'S1701_C01_001E': 'poverty_population_total',  # noqa: E501
                       'S1701_C02_001E': 'poverty_population_poverty',  # noqa: E501
                       'S1701_C02_002E': 'poverty_population_poverty_child'}  # noqa: E501
    poverty = CensusRequest('poverty', subject_table, poverty_metrics)

    actual_output_path = "tests/output/census_poverty_merged_actual_output.json"  # noqa: E501
    get_and_save_census_data([poverty], merged_output_path=actual_output_path, geo_ls=geo_ls, pretty_print=True)  # noqa: E501

    assert_file_contents_equal(actual_output_path, "tests/resources/census_poverty_merged_expected_output.json")  # noqa: E501
