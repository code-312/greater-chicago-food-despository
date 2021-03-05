<h2>ACS5 Scripts</h2>

*Scripts produce JSONs from ACS5 Census Data*

<u>To run:</u>

1. Obtain a Census API key [here](https://api.census.gov/data/key_signup.html)
2. Create a file called `.env` in the root directory. This file is ignored via the .gitignore file to avoid committing
   secrets.
3. Add the following to the `.env`:

```
CENSUS_KEY=REPLACE_ME_WITH_CENSUS_API_KEY
```

4. Run scripts:
    - test_jsons.py: runs all scripts and tests their output
        - Verifies scripts produce valid jsons
    - main.py: produces JSON files
        - To run with memory profiling on MacOS/Linux:
            1. Make sure the script is executable: `chmod 755 memory_profiling/run_main.sh`
            2. Run the script: `./memory_profiling/run_main.sh`
            3. View the report: `memory_profiling/memory_profile_report.txt`
        - To run with memory profiling on Windows (TODO need a Windows user to write this):
            1. Make sure the script is executable
            2. Run the script:
            3. View the report: `memory_profiling\memory_profile_report.txt`
<details>
<summary><u>ACS5 Data Tables</u></summary>

 - Detailed: https://api.census.gov/data/2018/acs/acs5?
   - "Most detailed cross-tabulations"
 - Subject: https://api.census.gov/data/2018/acs/acs5/subject?
   - "Overview of estimates available in a particular topic"
 - Data Profile: https://api.census.gov/data/2018/acs/acs5/profile?
   - "Broad social, economic, housing, and demographic information"
 - Comparison Profile: https://api.census.gov/data/2018/acs/acs5/cprofile?
   - "Similar to data profiles but include comparisons with past-year data"
</details>
JSON Format:

{'geographic area': {geo_code: {metric1_dict: {}, metric2_dict: {},...},...},...}

<hr>
<h3><u>How to use Main.py</u></h3>

- Add Census data call to script by creating new CensusData instance
    - Required Construction: CensusData(var_dict, table)
- Use the get_data method to update CensusData.df_dict
    - View dataframes: df_dict[key] (key='zip' or 'county')
- Save dataframe using CensusData.df_to_json()
    - Default saves zipped by geo_code
    - Set zip_df = False to save dataframes without processing
- Load dataframe using CensusData.load_df()
    - Default loads unzipped saved file, described above

<u>Additional Scripts</u>

**census_response.py**

*helper module for census API*

functions:

- **getCensusResponse**: creates census API query url
    - ACS5 Table URLs:
        - Detailed: https://api.census.gov/data/2018/acs/acs5/variables.html
        - Subject: https://api.census.gov/data/2018/acs/acs5/subject/variables.html
        - Data Profile: https://api.census.gov/data/2018/acs/acs5/profile/variables.html
        - Comparison Profile: https://api.census.gov/data/2018/acs/acs5/cprofile/variables.html
- **getCensusData**: obtains Census data returns as dictionary
    - Uses getCensusResponse for API call
    - By default runs for zip and county, but expandable to other geographies (not tested)
        - By default only keeps zipcodes for Illinois
- **searchTable**: searches variable tables with keyword and function filters
    - ACS5 Variable Table URLs:
        - Detailed: https://api.census.gov/data/2018/acs/acs5/variables.html
        - Subject: https://api.census.gov/data/2018/acs/acs5/subject/variables.html
        - Data Profile: https://api.census.gov/data/2018/acs/acs5/profile/variables.html
        - Comparison Profile: https://api.census.gov/data/2018/acs/acs5/cprofile/variables.html
- county_fips: returns JSON of county_name: fip (reversible)
- **processRaceData**: determines majority race and race percentages, passed into getCensusData function

**file_to_json.py**

*converts CSV and Excel files to the json format*

- County name in table MUST be in the first column or named "County Name"
- Returns list of JSON/Dictionaries to be merged

**dict_merge.py**

*Merges data dictionaries, prevents overwrite*

- Outputs to file and returns list of dictionaries
- Currently does not add missing data keys to geocodes
