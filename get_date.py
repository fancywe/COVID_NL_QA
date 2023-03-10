
from datetime import datetime
from pathlib import Path

import json
import os
import random
import sys
from os.path import exists
import requests
from state_code import state_codes


# url_all_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=county_view_state_data'
# url_county='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_external_data'
# url_county_vac='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_county_condensed_data'
# url_state='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_by_state_fips_'
# url_us='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=statusBar_v2_external_data'



def getDataFile(state,county,code):
    result={}
    data={}
    # date=datetime.today().strftime('%Y-%m-%d')   
    dic_name=''
  
    
    print(state,county,code)    
    headers = {'Accept': 'application/json'}
    
    
    if 2<=code<8:
                
        stateNum=state_codes[state]
        
        dic_name='integrated_county_latest_by_state_fips_'+stateNum
        path = 'json/State/'+stateNum+'/'
        lastFile=0
        dir_list = os.listdir(path)
        for x in dir_list:
            num=x.rsplit('.', 1)[0]
            num=int(num)
            if lastFile<num:lastFile=num
        lastFile=str(lastFile)    
        path=Path(path+lastFile+'.json')
        
            
        if(path.is_file()):
            with open(path) as json_file:
                data=json.load(json_file)
                json_object = json.loads(data)
           
            print(type(json_object))
            result= json_object[dic_name][0]
            
            return result
        
        # else:
        #     page = requests.get(url, headers=headers)

        #     text = json.loads(page.text)
        #     json_string =json.dumps(text)
            
        #     with open('json/State/State_'+stateNum+'_'+date+'.json', 'w') as outfile:
        #         json.dump(json_string, outfile)
                
                
    elif code==8:
        dic_name='county_view_state_data'
        path='json/Allstate/'
        lastFile=0
        dir_list = os.listdir(path)
        for x in dir_list:
            num=x.rsplit('.', 1)[0]
            num=int(num)
            if lastFile<num:
                lastFile=num
        lastFile=str(lastFile)
        print(lastFile)
        path=Path(path+lastFile+'.json')
        print(path)
        if(path.is_file()):
            with open(path) as json_file:
                data=json.load(json_file)
                json_object = json.loads(data)
           
            print(type(json_object))
        result= json_object[dic_name]
        return result
    
    elif 10<=code<20:
        
        
        dic_name='integrated_county_latest_external_data'  
        path = 'json/County/'
        lastFile=0
        dir_list = os.listdir(path)
        for x in dir_list:
            num=x.rsplit('.', 1)[0]
            num=int(num)
            if lastFile<num:
                lastFile=num
        lastFile=str(lastFile)
        print(lastFile)
        path=Path(path+lastFile+'.json')
        print(path)
        
        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            print(type(json_object))
            dic=json_object[dic_name]
            print(type(dic))
            for i in dic:
                if i["County"].lower()==(county.lower()+' county') and i["State"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' city') and i["State"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' muni') and i["State"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' parish') and i["State"]==state:
                        return i
        # else:
        #     page = requests.get(url, headers=headers)
    
        #     text = json.loads(page.text)
        #     print(type(text))
        #     json_string =json.dumps(text)
            
        #     with open('json/County/County_'+date+'.json', 'w') as outfile:
        #         json.dump(json_string, outfile)
        #         # json_object = json.load(outfile)
                
            # dic=text[dic_name] 
            
            # for i in dic:
            #     if i["County"].lower()==(county.lower()+' county') and i["State"]==state:
            #             return i
            #     elif i["County"].lower()==(county.lower()+' city') and i["State"]==state:
            #             return i
            #     elif i["County"].lower()==(county.lower()+' muno') and i["State"]==state:
            #             return i
            #     elif i["County"].lower()==(county.lower()+' parish') and i["State"]==state:
            #             return i
            
        
        return result
    
    elif code==15 :
        
        
        dic_name='vaccination_county_condensed_data'
        path ='json/County_Vac/'
        lastFile=0
        dir_list = os.listdir(path)
        for x in dir_list:
            num=x.rsplit('.', 1)[0]
            num=int(num)
            if lastFile<num:
             lastFile=num
        lastFile=str(lastFile)
        path=Path(path+lastFile+'.json')
        
        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            dic=json_object[dic_name]
            # print(county.lower(),state)
            for i in dic:
                if i["County"].lower()==(county.lower()+' county') and i["StateAbbr"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' city') and i["StateAbbr"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' muno') and i["StateAbbr"]==state:
                        return i
                elif i["County"].lower()==(county.lower()+' parish') and i["StateAbbr"]==state:
                        return i
            
        
        # else:
            
        #     page = requests.get(url, headers=headers)
    
        #     text = json.loads(page.text)
        #     json_string =json.dumps(text)
            
        #     with open('json/County_Vac/County_Vac_'+date+'.json', 'w') as outfile:
        #         json.dump(json_string, outfile)
        
                
        #     dic=text[dic_name]
            
        #     for i in dic:
        #         for i in dic:
        #             if i["County"].lower()==(county.lower()+' county') and i["StateAbbr"]==state:
        #                 return i
        #             elif i["County"].lower()==(county.lower()+' city') and i["StateAbbr"]==state:
        #                 return i
        #             elif i["County"].lower()==(county.lower()+' muno') and i["StateAbbr"]==state:
        #                 return i
        #             elif i["County"].lower()==(county.lower()+' parish') and i["StateAbbr"]==state:
        #                 return i
        #     # print(data)

        
        
    elif code==1:
            
            dic_name='statusbar'
            path ='json/US/'
            lastFile=0
            dir_list = os.listdir(path)
            for x in dir_list:
                num=x.rsplit('.', 1)[0]
                num=int(num)
                if lastFile<num:
                    lastFile=num
            lastFile=str(lastFile)
            path=Path(path+lastFile+'.json')
            
            if(path.is_file()):
                f=open(path)
                data=json.load(f)
                json_object = json.loads(data)
                dic=json_object[dic_name][0]
            return dic
                    
            # else:         
            #     page = requests.get(url, headers=headers)
        
            #     text = json.loads(page.text)
            #     json_string =json.dumps(text)
            #     with open(path, 'w') as outfile:
            #         json.dump(json_string, outfile)
                    
            #     dic=text[dic_name][0]
            #     return dic
            
    if code==20:
        result={'result':'Can\'t recognize the question'} 
        return result         
            
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
           