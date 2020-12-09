<u>ACS5 Scripts</u>

*Scripts produce JSONs from ACS5 Census Data*

To run:

1. Obtain a Census API key
2. Create api_keys.py in "greater-chicago-food-depository" root directory
3. In api_keys.py write "CENSUS_KEY = " and then paste your census key as a string ("")
4. Run scripts individually or all in one:
   - test_jsons.py: runs all scripts and tests their output
   - acs5countypoverty.py → acs5countypoverty_output.json
   - acs5zippoverty.py → acs5zippoverty_output.json
   - acs5racedeomgraphics.py → 
     - acs5countyrace_output.json
     - acs5ziprace_output.json



JSON Format:

{'geographic area': {metric1: data, metric2: data}}



<u>Additional Scripts</u>

**census_response.py**
*helper module for census API*
functions:

- getCensusResponse: creates census API query url
  - ACS5 Table URLs:
    - Detailed: https://api.census.gov/data/2018/acs/acs5?
      - "Most detailed cross-tabulations"
    - Subject: https://api.census.gov/data/2018/acs/acs5/subject?
      - "Overview of estimates available in a particular topic"
    - Data Profile: https://api.census.gov/data/2018/acs/acs5/profile?
      - "Broad social, economic, housing, and demographic information"
    - Comparison Profile: https://api.census.gov/data/2018/acs/acs5/cprofile?
      - "Similar to data profiles but include comparisons with past-year data"
- searchTable: searches variable tables with keyword and function filters
  - ACS5 Variable Table URLs:
    - Detailed: https://api.census.gov/data/2018/acs/acs5/variables.html
    - Subject: https://api.census.gov/data/2018/acs/acs5/subject/variables.html
    - Data Profile: https://api.census.gov/data/2018/acs/acs5/profile/variables.html
    - Comparison Profile: https://api.census.gov/data/2018/acs/acs5/cprofile/variables.html

