from numpy.lib.function_base import quantile
from src.config import CENSUS_KEY
import json
import requests
import numpy as np

def getCensusResponse(table_url,get_ls,geo):
    '''
    Concatenates url string and returns response from census api query
    input:
        table_url (str): census api table url
        get_ls (ls): list of tables to get data from
        geo (str): geographic area and filter
    output:
        response (requests.response): api response
    '''
    get = 'NAME,' + ",".join(get_ls)
    url = f'{table_url}get={get}&for={geo}&key={CENSUS_KEY}'
    # print(f"Calling for {geo}: {get_ls}")
    response = requests.get(url)
    # print(f"{response} Received")
    return(response)

class CensusData:
    df_dict = {}
    data_metrics = set()

    def __init__(self, var_metrics: tuple, table: str, geo_ls: list = ["zip", "county"]):
        self.metric = var_metrics[0]
        self.data_metrics.add(self.metric)
        self.var_dict = var_metrics[1]
        self.table = table
        self.geo_ls = geo_ls

    def get_data(self):
        geo_dict = {'zip': 'zip code tabulation area:*',
                    'county': 'county:*&in=state:17'}
        get_ls = list(self.var_dict.keys())
        df_ls = []
        for g in self.geo_ls:
            response = getCensusResponse(self.table, get_ls, geo_dict[g])
            self.response_json = jsonResponse(response)
            df = self.__panda_from_json(self.response_json, g)
            df_ls.append(df)
        return df_ls

    def __panda_from_json(self, response_json, geo):
        '''
        Called by getData method
        Updates CensusData.zip_df and returns response_df
        '''
        # Name Columns
        # hard coded columns are default from census response
        # only works if we're only processing zip and county data
        dict_values = list(self.var_dict.values())
        columns = [self.var_dict.get(header, header)
                   for header in response_json[0]]
        #print(columns, response_json[0])
        # Creates DF
        response_df = pd.DataFrame(response_json[1:], columns=columns)
        # adds types for performance and predictable method output
        string_df = response_df.astype('string')
        # ignore error to keep NAN values
        typed_df = string_df.astype(
            {v: int for v in dict_values}, errors='ignore')
        # Processes geographies for output
        if geo == 'county':
            fip_series = typed_df.loc[:, 'state'] + typed_df.loc[:, 'county']
            fip_series.rename('FIPS', inplace=True)
            geo_df = pd.concat([typed_df, fip_series], axis=1)
            geo_df = geo_df.set_index('FIPS').drop(['state', 'county'], axis=1)
            #self.county_df = self.county_df.join(geo_df, how='outer') if not(self.county_df.empty) else geo_df
        elif geo == 'zip':
            # filter keeps Illinois zipcodes
            # zip sometimes returns with 'state' column, so it isn't dropped atm
            geo_df = typed_df.set_index('zip code tabulation area').drop(
                ['NAME'], axis=1).filter(regex='^(6[0-2])\d+', axis=0)

        class_df = self.df_dict.get(geo, pd.DataFrame())
        if not(class_df.empty):
            geo_df = geo_df.drop(
                ['NAME'], axis=1) if 'NAME' in class_df.columns else geo_df
            try:
                self.df_dict[geo] = class_df.join(geo_df, how='outer')
            except Exception as e:
                print(e)
                print("Make sure the column names are unique")
        else:
            self.df_dict[geo] = geo_df

        return geo_df

    @classmethod
    def df_to_json(cls, zip_df = True):
        if not(zip_df):
            k_json = dict()
            fp = 'final_jsons/df_dump.json'
            for k in cls.df_dict:
#                 fp = f'final_jsons/{k}_df_dump.json'
#                 k_json = cls.df_dict[k].to_json()
                #with open(fp, 'w') as f:
                k_json[k] = cls.df_dict[k].to_dict()
            
            with open(fp, 'w') as f:
                json.dump(k_json, f, separators=(',', ':'))
                    #json.dumps(k_json, f, separators=(',', ':'))
            return fp
        # determine metrics
        class_json_dict = dict()
        for geo in cls.df_dict:
            geo_dict = dict()
            for geo_area in cls.df_dict[geo].itertuples():
                geo_area_dict = {f'{m}_data': dict() for m in cls.data_metrics}
                for name in geo_area._fields:
                    if name == "Index":
                        continue
                    for metric in cls.data_metrics:
                        metric_name = f'{metric}_data'
                        geo_area_dict[metric_name]
                        if metric in name:
                            geo_area_dict[metric_name][name] = getattr(
                                geo_area, name)
                            break
                    else:
                        geo_area_dict[name] = getattr(geo_area, name)
                geo_dict[geo_area.Index] = geo_area_dict
            class_json_dict[geo] = geo_dict
        fp = 'final_jsons/df_merged_json.json'
        with open(fp, 'w') as f:
            json.dump(class_json_dict, f, separators=(',', ':'))

        return fp
    
    @classmethod
    def load_df(cls, fp='final_jsons/df_dump.json'):
        with open(fp) as f:
            load_df = json.load(f)
        
        cls.df_dict = dict()
        
        for k in load_df:
            v = pd.DataFrame(load_df[k])
            cls.df_dict[k] = v
        
        return None

def getCensusData(table_code_dict, census_table, function_ls = [], geo_ls=["zip","county"]):

    '''
    Obtains Census data and returns zip and county dictionaries
    input:
        table_code_dict (dict):
            Key: Census Table Variable (str)
            Value: Descriptive name of variable (str)
        census_table (str, url): Census table url
        geo_ls (ls): Geographies to return, accepts "zip" and "county" as keywords
                    additional geographies may be passed, but must be valid Census API keywords
        function_ls (ls): functions to run sequentially on final_js, before saved and returned
    output:
        final_json (dict):
            key: zip or county code (str)
            value: metrics (dict)
                key: metric name (str)
                value: metric value (object)
    '''
    final_json_ls = []
    for geography in geo_ls:
        if geography == 'zip':
            geo = 'zip code tabulation area:*'
        elif geography == 'county':
            geo = 'county:*&in=state:17'
        else:
            raise Exception(f"Invalid Geography: {geography}")

        key_ls = list(table_code_dict.keys())
        value_ls = list(table_code_dict.values())
        #Values name format: topic_property_subproperty
        topic = value_ls[0].split('_')[0]
        value_ls.insert(0, 'name')
        value_ls.append('g')

        response = getCensusResponse(census_table, key_ls, geo)

        try:
            response_data = response.json()
        except Exception as e:
            print(e)
            print(response_data)
            raise e
        #Replaces Census table IDs with labels
        labelled_ls = [[]]

        for i, row in enumerate(response_data):
            #header row
            if i == 0:
                for c, col in enumerate(response_data[0]):
                    #Gets variable label from group data
                    #Otherwise adds column name
                    label = table_code_dict.get(col, col)
                    labelled_ls[0].append(label)
            #converts data strings to ints
            else:
                new_row = []
                for v, n in enumerate(row):
                    #First and last elements are geo names
                    if v == 0 or v == len(row)-1:
                        new_row.append(n)
                    #Tries to convert data to int
                    else:
                        try:
                            new_row.append(int(n))
                        except:
                            #Value likely null
                            new_row.append(n)

                labelled_ls.append(new_row)
        
        #breakpoint()
        IL_data = []
        
        if "zip" == geography:
        #filter zipcodes
        #IL zipcodes begin with numbers in zip_ls_IL
            zip_ls_IL = ['60', '61', '62']

            for d in labelled_ls[1:]:
                #print(d[3][:2])
                if d[-1][:2] in zip_ls_IL:
                    IL_data.append(d)
        else:
            #creates county geo labels
            IL_data = [d[:-2] + [f"{d[-2]}{d[-1]}"] for d in labelled_ls[1:]]
        final_json = {geography:{}}

        for d in IL_data:
            
            #create geography json
            #topic_metrics nests topic data
            geo_dict = {l:d[i] for i, l in enumerate(value_ls)}
            
            g_json = {f'name_{geography}': geo_dict['name'], f'{topic}_metrics': geo_dict}

            #set geography key to geography json value
            final_json[geography][geo_dict['g']] = g_json

        for f in function_ls:
            final_json[geography] = f(final_json[geography])

        #save file
        # print("Final Json created, saving to file")
        # breakpoint()
        with open(F'final_jsons/acs5{geography}{topic}_output.json', 'w') as f:
            json.dump(final_json, f, separators=(',',':'))
        
        final_json_ls.append(final_json)
    return final_json_ls

def searchTable(table_json_ls: list, keyword_ls: list, filter_function_ls: list) -> list:
    '''
    Filters variable tables by keyword and filter
    input:
        table_json_ls (response.json() list object): list of lists from census variable table api
        keyword_ls (list):  list of keyword strings
                            keyword filter applied to the third element of the input list (concept column)
        filter_function_ls (list): list of functions that filter table_json_ls with filter method
    output:
        return_json_ls (list): list, same format as table_json_ls, filtered
    '''    
    return_json_ls = list()
    
    #runs filter for each function in filter_function_ls
    for f in filter_function_ls:
        table_json_ls = list(filter(f, table_json_ls))
    
    #adds rows with keyword(s) in concept column to return_json_ls
    for d in table_json_ls:
        try:
            for k in keyword_ls:
                #d[2] is the concept column, d[1] is the label column
                if k.lower() in d[2].lower() or k.lower() in d[1].lower():
                    continue
                else:
                    break
            else:
                return_json_ls.append(d)
        except: 
            continue
    
    return return_json_ls

def county_fips(reverse = False) -> dict:
    '''
    Requests county fips from census API and returns list of IL county FIPS
    input: reverse (bool) reverses keys and values in output
    output: il_json (dict) {'county name': 'fip'}
    '''
    import requests

    url = 'https://api.census.gov/data/2010/dec/sf1?get=NAME&for=county:*'

    response = requests.get(url)

    #filter for IL
    il_county = lambda x: x[1] == '17'

    response_json = response.json()

    if reverse:
        il_json = {county[1]+county[2]: county[0]  for county in response_json if il_county(county)}
    else:
        il_json = {county[0]: county[1]+county[2] for county in response_json if il_county(county)}

    return il_json

def processRaceData(data_json):
    '''
    Determines majority race and race percentages from getRaceData final json and adds to race_metrics
    input:
        data_json (dict): final_json from getRaceData
    output:
        data_json (dict): input with 'race_majority' and 'percentages' metrics added to 'race_metrics'
    '''
    #Majority filter function
    majority = lambda x, y: x/y >= 0.5

    for d in data_json.items():
        #race_majority default value, since another majority would overwrite
        race_majority = "majority_minority"
        race_data = d[1]['race_metrics']
        race_total = race_data['race_total']
        percentages = {}
        #if: checks that total is not zero
        if race_total:
            for k, v in race_data.items():
                #skips evaluating race_total, 'name' and 'g'
                try:
                    skip_ls = ['race_total','name','g']
                    if k in skip_ls:
                        continue
                    elif majority(v,race_total):
                        race_majority = k
                    #Add percentage
                    race_pct = v/race_total * 100
                    percentages[k] = race_pct
                except Exception as e:
                    print(e) #error
                    print(d) #current data object
                    print(race_data) #racemetrics
                    print(v, race_total) #race data value, race_total metric
                    raise Exception('Error')
        #Add majority and percentages to json
        data_json[d[0]]['race_metrics']['race_majority'] = race_majority
        data_json[d[0]]['race_metrics']['percentages'] = percentages
        #For dev investigation if printed
        if race_majority == 'race_other' or race_majority == 'race_twoplus_exclusive':
            print(d)
    
    return data_json

def processPovertyData(data_json):
    '''
    Calculates percent poverty
    data_json (dict)
    '''
    from collections import defaultdict
    pct_dict = defaultdict(list)
    for d in data_json.items():
        poverty_data = d[1]['poverty_metrics']
        poverty_total = poverty_data['poverty_population_total']
        percentages = {}
        if poverty_total:
            for k, v in poverty_data.items():
                #skips evaluating poverty_population_total, 'name' and 'g'
                try:
                    skip_ls = ['poverty_population_total','name','g']
                    if k in skip_ls:
                        continue
                    #Add percentage
                    poverty_pct = v/poverty_total * 100
                    percentages[k] = poverty_pct
                    pct_dict[k].append(poverty_pct)
                    
                except Exception as e:
                    print(e) #error
                    print(d) #current data object
                    print(poverty_data) #povertymetrics
                    print(v, poverty_total) #poverty data value, poverty_total metric
                    raise Exception('Error')
            else:
                pct_dict[k] = np.array(pct_dict[k])
        data_json[d[0]]['poverty_metrics']['percentages'] = percentages
    else:
        pct_bin = binData(pct_dict)
        #breakpoint()
        data_json['meta'] = data_json.get('meta',{})
        data_json['meta']['poverty_bins'] = pct_bin
    return data_json

def binData(geoData: dict):
    '''
    Creates bins from functions described in this function 
    
    geoData:
        keys: geo code
        values: percentages or data to bin
    '''

    def quartiles(geoValue):
        min_v = np.min(geoValue)
        first = np.quantile(geoValue, 0.25)
        second = np.quantile(geoValue, 0.5)
        third = np.quantile(geoValue, 0.75)
        max = np.max(geoValue)
        q = [min_v, first, second, third, max]
        
        return {'quartiles': q}
    
    bin_dict = {}
    
    for k in geoData:
        v = geoData[k]
        try:
            q = quartiles(v)
        except:
            continue
        bin_dict[k] = q

    return bin_dict