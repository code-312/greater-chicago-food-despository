# Data Pipeline

Running src/main.py reads in data from the US census API and local files containing data about child nutrition programs, food insecurity, SNAP usage and WIC usage. The script outputs three JSON files that can be used with the [front end project](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui) and CSV files of the WIC data which was originally requested by the Greater Chicago Food Depository.

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

### Child Nutrition Programs Data

The project reads the number of breakfast, lunch, afterschool and Summer Food Service Program meals served from an Excel spreadsheet provided by the Greater Chicago Food Depository.

### Food Insecurity Data

The project reads child and total food insecurity rates from 2018 as well as projected 2020 data from an Excel spreadsheet provided by the Greater Chicago Food Depository.

### SNAP Usage Data

THe project reads SNAP usage data from Excel spreadsheets provided by the Greater Chicago Food Depository. There is one spreadsheet for 2019 and one for 2020. The data is broken down by age and race.

### WIC Usage Data

The project parses WIC usage data from a PDF supplied by the Greater Chicago Food Depository. These counties are missing from the PDF and it is unclear why: Edwards, Menard, Perry, Pope, Stark, and Williamson.

## Output

The main output of the script is three JSON files: countyData.json, metaData.json and zipData.json. When the version number in `src.main` is updated, these JSON files are compressed into a zip file.

### countyData.json

countyData.json is a dictionary where the keys are [county FIPS codes](https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697). All Illinois FIPS codes start with "17".

The values in the dictionary follow this schema:

```javascript
{
	"NAME": "Adams County, Illinois",
	"child_nutrition_data": {
		"2019": {
			"afterschool_meals_count": 23197.0,
			"breakfast_count": 475110.0,
			"lunch_count": 1131503.0,
			"sfsp_count": 18035.0
		}
	},
	"insecurity_data": {
		"insecurity_2018": 0.102,
		"insecurity_2018_child": 0.142,
		"insecurity_2020_child_projected": 0.206,
		"insecurity_2020_projected": 0.135
	},
	"poverty_data": {
		"poverty_percentages": {
			"poverty_population_poverty": 0.12143,
			"poverty_population_poverty_child": 0.036781
		},
		"poverty_population_poverty": 7874,
		"poverty_population_poverty_child": 2385,
		"poverty_population_total": 64844
	},
	"race_data": {
		"race_asian": 540,
		"race_black": 2676,
		"race_hispaniclatino_total": 1021,
		"race_majority": "race_white",
		"race_native": 178,
		"race_other": 72,
		"race_pacific": 42,
		"race_percentages": {
			"race_asian": 0.008129,
			"race_black": 0.040285,
			"race_hispaniclatino_total": 0.01537,
			"race_native": 0.00268,
			"race_other": 0.001084,
			"race_pacific": 0.000632,
			"race_twoplus_total": 0.013383,
			"race_white": 0.918437
		},
		"race_total": 66427,
		"race_twoplus_total": 889,
		"race_white": 61009
	},
	"snap_data": {
		"2019": {
			"age_0-4": {
				"race_asian": 6.0,
				"race_black": 175.0,
				"race_hispaniclatino": 24.0,
				"race_native": 3.0,
				"race_pacific": 4.0,
				"race_unknown": 516.0,
				"race_white": 572.0
			},
			"age_18-65": {
				"race_asian": 16,
				"race_black": 741,
				"race_hispaniclatino": 60,
				"race_native": 20,
				"race_pacific": 6,
				"race_unknown": 295,
				"race_white": 4417
			},
			"age_5-17": {
				"race_asian": 5.0,
				"race_black": 273.0,
				"race_hispaniclatino": 64.0,
				"race_native": 10.0,
				"race_pacific": 7.0,
				"race_unknown": 1091.0,
				"race_white": 1235.0
			},
			"age_66+": {
				"race_asian": 4.0,
				"race_black": 46.0,
				"race_hispaniclatino": 6.0,
				"race_native": 0.0,
				"race_pacific": 0.0,
				"race_unknown": 12.0,
				"race_white": 569.0
			}
		},
		"2020": {
			"age_0-4": {
				"race_asian": 5.0,
				"race_black": 164.0,
				"race_hispaniclatino": 27.0,
				"race_native": 2.0,
				"race_pacific": 4.0,
				"race_unknown": 563.0,
				"race_white": 591.0
			},
			"age_18-65": {
				"race_asian": 17.0,
				"race_black": 812.0,
				"race_hispaniclatino": 97.0,
				"race_native": 25.0,
				"race_pacific": 10.0,
				"race_unknown": 381.0,
				"race_white": 5100.0
			},
			"age_5-17": {
				"race_asian": 14.0,
				"race_black": 295.0,
				"race_hispaniclatino": 81.0,
				"race_native": 9.0,
				"race_pacific": 6.0,
				"race_unknown": 1207.0,
				"race_white": 1378.0
			},
			"age_66+": {
				"race_asian": 5.0,
				"race_black": 65.0,
				"race_hispaniclatino": 7.0,
				"race_native": 1.0,
				"race_pacific": 0.0,
				"race_unknown": 14.0,
				"race_white": 643.0
			}
		}
	},
	"wic_participation_children_data": {
		"hispanic_or_latino": 20,
		"race_amer_indian_or_alaskan_native": 3,
		"race_asian": 1,
		"race_black": 97,
		"race_multiracial": 51,
		"race_native_hawaii_or_pacific_islander": 3,
		"race_white": 322,
		"total": 365
	},
	"wic_participation_infants_data": {
		"hispanic_or_latino": 19,
		"race_amer_indian_or_alaskan_native": 1,
		"race_asian": 3,
		"race_black": 54,
		"race_multiracial": 38,
		"race_native_hawaii_or_pacific_islander": 3,
		"race_white": 216,
		"total": 237
	},
	"wic_participation_total_data": {
		"hispanic_or_latino": 44,
		"race_amer_indian_or_alaskan_native": 4,
		"race_asian": 6,
		"race_black": 172,
		"race_multiracial": 95,
		"race_native_hawaii_or_pacific_islander": 8,
		"race_white": 697,
		"total": 780
	},
	"wic_participation_women_data": {
		"hispanic_or_latino": 5,
		"race_amer_indian_or_alaskan_native": 0,
		"race_asian": 2,
		"race_black": 21,
		"race_multiracial": 6,
		"race_native_hawaii_or_pacific_islander": 2,
		"race_white": 159,
		"total": 178
	}
}
```

### metaData.json

metaData.json is an object with two fields: "data_bins" and "data_metrics".

#### data_bins

data_bins has two fields "natural_breaks" and "quantiles" that describe how the divide the data into five bins using either [Jenks natural breaks](https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization) or [quantiles](https://en.wikipedia.org/wiki/Quantile).

"natural_breaks" and "quantiles" follow the same schema as the data for a single county, but instead of a data point, they include a list of six values separating the bins for that specific data metric.

The data for a group of five bins could look like this:

```javascript
[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
```

For that data, the bins would be:

Bin Name | Range of Values
-------------- | --------------
Bin 1 | 0.0 - 0.2
Bin 2 | 0.2 - 0.4
Bin 3 | 0.4 - 0.6
Bin 4 | 0.6 - 0.8
Bin 5 | 0.8 - 1.0

#### data_metrics

data_metrics is an object with one dictionary "poverty" that maps the census variables used to internal names and another dictionary "race" that does the same for race census variables.

### zipData.json

zipData.json is similar to countyData.json, but zipData.json uses ZIP codes as the keys and the values only contain the "poverty_data" and "race_data" fields. This is because all the input data except for census data was only available per county.

### How to Update the Data in the Front End

Take the outputted JSON files and update the versions in the [fetched_data folder](https://github.com/Code-For-Chicago/greater-chicago-food-despository-ui/tree/main/src/fetched_data) in the front end repository.
