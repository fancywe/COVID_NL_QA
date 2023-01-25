
from datetime import datetime
from pathlib import Path
import spacy
import json
import os
import random
import sys
from os.path import exists
import requests
from state_code import state_codes

def getDataFile(state,county,qtype):
    result={}
    data={}
    date=datetime.today().strftime('%Y-%m-%d')
    # p_len = 4
    # url_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=county_view_state_data'
    url_county='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_external_data'
    url_county_vac='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_county_condensed_data'
    url_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_by_state_fips_'
    url_us='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=statusBar_v2_external_data'
    # qtype=sys.argv[1]
    # state=sys.argv[2]
    # county=''
    
    dic_name=''
    print(type(data))
    if(county!=''):
        county+=' County'
    print(state,county,qtype)    
    headers = {'Accept': 'application/json'}
    
    
    if qtype==100:
        result={'result':'Can\'t recognize the question'} 
        return result 
    
    if qtype==1 or qtype==4:
                
        stateNum=state_codes[state]
        url=url_state+stateNum
        dic_name='integrated_county_latest_by_state_fips_'+stateNum
        path = Path('json/State/State_'+stateNum+'_'+date+'.json')

        if(path.is_file()):
            with open(path) as json_file:
                data=json.load(json_file)
                json_object = json.loads(data)
           
            print(type(json_object))
            result= json_object[dic_name][0]
            
            return result
        
        else:
            page = requests.get(url, headers=headers)

            text = json.loads(page.text)
            json_string =json.dumps(text)
            
            with open('json/State/State_'+stateNum+'_'+date+'.json', 'w') as outfile:
                json.dump(json_string, outfile)
                
                
            dic=text[dic_name][0]
            # print(data)
            
            
            
            return dic
        
    elif qtype==2:
        
        url=url_county    
        dic_name='integrated_county_latest_external_data'  
        path = Path('json/County/County_'+date+'.json')

        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            print(type(json_object))
            dic=json_object[dic_name]
            print(type(dic))
            for i in dic:
                if i["County"].lower()==county.lower() and i["State"]==state:
                    return i
            
           
        else:
            page = requests.get(url, headers=headers)
    
            text = json.loads(page.text)
            print(type(text))
            json_string =json.dumps(text)
            
            with open('json/County/County_'+date+'.json', 'w') as outfile:
                json.dump(json_string, outfile)
                # json_object = json.load(outfile)
                
            dic=text[dic_name] 
            
            for i in dic:
                if i["County"].lower()==county.lower() and i["State"]==state:
                    return i
            
        
            return result
    
    elif qtype==3 :
        
        url=url_county_vac
        dic_name='vaccination_county_condensed_data'
        path = Path('json/County_Vac/County_Vac_'+date+'.json')
        
        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            dic=json_object[dic_name]
            # print(county.lower(),state)
            for i in dic:
                if (i["County"].lower()==county.lower())and (i["StateAbbr"]==state):
                    print(i)
                    return i
            
        
        else:
            
            page = requests.get(url, headers=headers)
    
            text = json.loads(page.text)
            json_string =json.dumps(text)
            
            with open('json/County_Vac/County_Vac_'+date+'.json', 'w') as outfile:
                json.dump(json_string, outfile)
        
                
            dic=text[dic_name]
            
            for i in dic:
                if i["County"].lower()==county.lower() and i["StateAbbr"]==state:
                    return i
            # print(data)

            return result
        
    elif qtype==5:
            url=url_us
            dic_name='statusbar'
            path = Path('json/US/US'+date+'.json')
            
            if(path.is_file()):
                f=open(path)
                data=json.load(f)
                json_object = json.loads(data)
                dic=json_object[dic_name][0]
                return dic
                    
            else:         
                page = requests.get(url, headers=headers)
        
                text = json.loads(page.text)
                json_string =json.dumps(text)
                with open(path, 'w') as outfile:
                    json.dump(json_string, outfile)
                    
                dic=text[dic_name][0]
                return dic
            
            
    # else:
        
    #     stateNum=state_codes[state]
    #     url=+stateNum
    #     dic_name='integrated_county_latest_by_state_fips_'+stateNum
    #     path = Path('json/State_Vac/State_Vac'+date+'.json')
        
    #     if(path.is_file()):
    #         data=json.load(path)
    #         dic=data[dic_name]
            
    #         return dic
        
    #     else:
            
    #         page = requests.get(url, headers=headers)
    
    #         data = json.loads(page.text)
    #         json_string =json.dumps(data)
            
    #         with open('json/State_Vac/State_Vac'+date+'.json', 'w') as outfile:
    #             json.dump(json_string, outfile)
    #         # print(data)
            
    #         dic=data[dic_name]
    #         # result=dict(filter(lambda x:x["County"]==county and x['StateAbbr']==state,dic))
    #         return dic 
           