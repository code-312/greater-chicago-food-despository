# Data Pipeline

## Input

### Census Data

The project downloads race and poverty demographic data from the 2018 US census. It uses the census API to download data about each zipcode and county in Illinois.

The project uses these census variables:

Census Variable | Internal Name
-------------- | --------------
B03002_001E | race_total
B03002_005E | race_native
B03002_004E | race_black
B03002_003E | race_white
B03002_009E | race_twoplus_total
B03002_007E | race_pacific
B03002_008E | race_other
B03002_006E | race_asian
B03002_012E | race_hispaniclatino_total
S1701_C01_001E | poverty_population_total
S1701_C02_001E | poverty_population_poverty
S1701_C02_002E | poverty_population_poverty_child

### Child Nutrition Data



### Food Insecurity Data

### SNAP Usage Data

### WIC Usage Data

The project parses WIC usage data from a PDF supplied by the Greater Chicago Food Depository.

## Output

Running src/main.py outputs three JSON files that can be used with the front end project and CSV files of the WIC data which was originally requested by the Greater Chicago Food Depository.

### countyData.json

### metaData.json

### zipData.json
