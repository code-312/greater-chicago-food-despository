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

The project parses WIC usage data from a PDF supplied by the Greater Chicago Food Depository. These counties are missing from the PDF and it is unclear why: Edwards, Menard, Perry, Pope, Stark, and Williamson.

## Output

Running src/main.py outputs three JSON files that can be used with the [front end project](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui) and CSV files of the WIC data which was originally requested by the Greater Chicago Food Depository.

### countyData.json

### metaData.json

### zipData.json

### How to Update the Data in the Front End

Take the outputted JSON files and update the versions in the [fetched_data folder](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui/tree/main/src/fetched_data) in the front end repository.
