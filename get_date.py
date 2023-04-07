
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
    
    
    if 1<=code<7:
                
        stateNum=state_codes[state]
        
        dic_name='integrated_county_latest_by_state_fips_'+stateNum
        path = 'json/State/'+stateNum+'/'
        # lastFile=0
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:lastFile=num
        # lastFile=str(lastFile)    
        path=Path(path+'state'+'.json')
        
            
        if(path.is_file()):
            with open(path) as json_file:
                data=json.load(json_file)
                json_object = json.loads(data)
           
            print(type(json_object))
            result= json_object[dic_name][0]
        history='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_timeseries_by_state_fips_'+str(stateNum)
        page = requests.get(history, headers=headers) # get county
        text = json.loads(page.text)
        dic_name="integrated_county_timeseries_by_state_fips_"+str(stateNum)
        result['History']=text[dic_name] 
          
        return result
        
        # else:
        #     page = requests.get(url, headers=headers)

        #     text = json.loads(page.text)
        #     json_string =json.dumps(text)
            
        #     with open('json/State/State_'+stateNum+'_'+date+'.json', 'w') as outfile:
        #         json.dump(json_string, outfile)
                
                
    elif code==7:
        dic_name='county_view_state_data'
        path='json/Allstate/'
        lastFile=0
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:
        #         lastFile=num
        # lastFile=str(lastFile)
        # print(lastFile)
        path=Path(path+'AllState'+'.json')
        print(path)
        if(path.is_file()):
            print('hi')
            with open(path) as json_file:
                data=json.load(json_file)
                json_object = json.loads(data)
           
            print(type(json_object))
        result= json_object[dic_name]
       
        return result
    
    elif 10<=code<15:
        
        
        dic_name='integrated_county_latest_external_data'  
        path = 'json/County/'
        lastFile=0
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:
        #         lastFile=num
        # lastFile=str(lastFile)
        # print(lastFile)
        path=Path(path+'County'+'.json')
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
                        result=i
                elif i["County"].lower()==(county.lower()+' city') and i["State"]==state:
                        result=i
                elif i["County"].lower()==(county.lower()+' muni') and i["State"]==state:
                        result=i
                elif i["County"].lower()==(county.lower()+' parish') and i["State"]==state:
                        result=i
                    
            fips=result['fips_code']
            print(fips)
            history='https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_timeseries_fips_'+str(fips)+'_external'
            page = requests.get(history, headers=headers) # get county
            text = json.loads(page.text)
            result['History']=text["integrated_county_timeseries_external_data"] 
                       
        return result
    
    elif code==8 :
        
        dic_name='integrated_county_latest_external_data'  
        path = 'json/County/'
        lastFile=0
        resultList=[]
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:
        #         lastFile=num
        # lastFile=str(lastFile)
        # print(lastFile)
        path=Path(path+'County'+'.json')
        print(path)
        
        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            print(type(json_object))
            dic=json_object[dic_name]
            print(type(dic))
            for i in dic:
                
                    result={'State':i['State_name'],'County':i['County'],'Level':i['CCL_community_burden_level'],'New Case Past 7 days':i['Cases_7_day_count_change'],
                        'New Case Rate Past 7 days (100K)':i['cases_per_100K_7_day_count_change'],
                        'New Case Rate changed':i['new_cases_week_over_week_percent_change'],
                        'New Death Past 7 days':i['deaths_7_day_count_change'],
                        '7 days Death rate in 100K':i['deaths_per_100K_7_day_count_change'],
                        '7 days Death changed ':i['new_deaths_week_over_week_percent_change'],
                        'Total Postive last week':i['percent_test_results_reported_positive_last_7_days']
                        ,'Total Postive changed':i['percent_test_results_reported_positive_last_7_days_7_day_count_change'],
                        'Postive Population rate in 100K':i['total_test_results_reported_7_day_count_change_per_100K'],
                        'Postive Population rate in 100K changed':i['total_new_test_results_reported_week_over_week_percent_change'],
                        'New Admissions last 7 days':i['admissions_covid_confirmed_last_7_days'],
                        'New Admissions changed':i['admissions_covid_confirmed_week_over_week_percent_change'],
                        'COVID Inpatient Beds Used':i['percent_adult_inpatient_beds_used_confirmed_covid'],
                        'COVID Inpatient Beds Used changed':i['percent_adult_inpatient_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        'ICU Beds Used by Covid':i['percent_adult_icu_beds_used_confirmed_covid'],
                        'ICU Beds Used by Covid changed':i['percent_adult_icu_beds_used_confirmed_covid_week_over_week_absolute_change']}
                    resultList.append(result)
            
            print(resultList)
            return resultList
                    
    elif code==15 :
        
        
        dic_name='vaccination_county_condensed_data'
        path ='json/County_Vac/'
        # lastFile=0
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:
        #      lastFile=num
        # lastFile=str(lastFile)
        path=Path(path+'County_Vac'+'.json')
        
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
                    
    elif code==0:
            
            dic_name='statusbar'
            path ='json/US/'
            lastFile=0
            dir_list = os.listdir(path)
            # for x in dir_list:
            #     num=x.rsplit('.', 1)[0]
            #     num=int(num)
            #     if lastFile<num:
            #         lastFile=num
            # lastFile=str(lastFile)
            path=Path(path+'US'+'.json')
            
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
    elif code==9:
        dic_name='integrated_county_latest_external_data'  
        path = 'json/County/'
        lastFile=0
        resultList=[]
        # dir_list = os.listdir(path)
        # for x in dir_list:
        #     num=x.rsplit('.', 1)[0]
        #     num=int(num)
        #     if lastFile<num:
        #         lastFile=num
        # lastFile=str(lastFile)
        # print(lastFile)
        path=Path(path+'County'+'.json')
        print(path)
        
        if(path.is_file()):
            f=open(path)
            data=json.load(f)
            json_object = json.loads(data)
            print(type(json_object))
            dic=json_object[dic_name]
            print(type(dic))
            for i in dic:
                if  i["State"]==state:
                    result={'State':i['State_name'],'County':i['County'],'Level':i['CCL_community_burden_level'],'New Case Past 7 days':i['Cases_7_day_count_change'],
                        'New Case Rate Past 7 days (100K)':i['cases_per_100K_7_day_count_change'],
                        'New Case Rate changed':i['new_cases_week_over_week_percent_change'],
                        'New Death Past 7 days':i['deaths_7_day_count_change'],
                        '7 days Death rate in 100K':i['deaths_per_100K_7_day_count_change'],
                        '7 days Death changed ':i['new_deaths_week_over_week_percent_change'],
                        'Total Postive last week':i['percent_test_results_reported_positive_last_7_days']
                        ,'Total Postive changed':i['percent_test_results_reported_positive_last_7_days_7_day_count_change'],
                        'Postive Population rate in 100K':i['total_test_results_reported_7_day_count_change_per_100K'],
                        'Postive Population rate in 100K changed':i['total_new_test_results_reported_week_over_week_percent_change'],
                        'New Admissions last 7 days':i['admissions_covid_confirmed_last_7_days'],
                        'New Admissions changed':i['admissions_covid_confirmed_week_over_week_percent_change'],
                        'COVID Inpatient Beds Used':i['percent_adult_inpatient_beds_used_confirmed_covid'],
                        'COVID Inpatient Beds Used changed':i['percent_adult_inpatient_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        'ICU Beds Used by Covid':i['percent_adult_icu_beds_used_confirmed_covid'],
                        'ICU Beds Used by Covid changed':i['percent_adult_icu_beds_used_confirmed_covid_week_over_week_absolute_change']}
                    resultList.append(result)
            
            print(resultList)
            return resultList
            
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
           