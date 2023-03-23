#!/usr/bin/python3
#-*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import time
import json
import os
import random
import sys
from os.path import exists
import requests

url_all_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=county_view_state_data'
url_county='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_external_data'
url_county_vac='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_county_condensed_data'
url_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_by_state_fips_'
url_us='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=statusBar_v2_external_data'

history_1='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_timeseries_by_state_fips_06'
history_2='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_timeseries_fips_06033_external'
vac_detail='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data'

headers = {'Accept': 'application/json'}


page = requests.get(url_all_state, headers=headers) # get all state
text = json.loads(page.text)

# runid=str(text["runid"])
json_string =json.dumps(text)

with open('json/AllState/AllState.json', 'w') as outfile:
            json.dump(json_string, outfile)   
time.sleep(2)

            
page = requests.get(url_county, headers=headers)  # get county vac
text = json.loads(page.text)
print(type(text))
runid=str(text["runid"])
json_string =json.dumps(text)

with open('json/County/County.json', 'w') as outfile:
            json.dump(json_string, outfile)  
time.sleep(2)

            
page = requests.get(url_county_vac, headers=headers) # get county
text = json.loads(page.text)

# runid=str(text["runid"])
json_string =json.dumps(text)

with open('json/County_Vac/County_Vac.json', 'w') as outfile:
            json.dump(json_string, outfile)    

for i in range(1,57):  
        
    stateNum=format(i, '02d')   
    url=url_state+stateNum
    filename='json/State/'+stateNum+'/state.json'
    path = Path(filename)
    
    if(path.is_file()): continue
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)      
    page = requests.get(url, headers=headers) # get url_state
    if page.ok:
        text = json.loads(page.text)
        print(text)
        # runid=str(text["runid"])
        json_string =json.dumps(text)
        
        with open(filename, 'w') as outfile:
                    json.dump(json_string, outfile)     
        time.sleep(3)     

page = requests.get(url_us, headers=headers) # get url_us
text = json.loads(page.text)

# runid=str(text["runid"])
json_string =json.dumps(text)

with open('json/US/US.json', 'w') as outfile:
            json.dump(json_string, outfile)                                        
                                                               
                      
            