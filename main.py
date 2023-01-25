from get_date import getDataFile
import spacy
import json
import os
import random
import sys
from os.path import exists
import requests
from datetime import datetime
import state_code
from pathlib import Path




from fastapi import FastAPI

from county_code import countyName

nlp =spacy.load('en_core_web_sm')

# sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='unicode ', buffering=1)
# filename="fips-codes-covid-tracker.csv"
# csvfile=open("fips-codes-covid-tracker.csv")
# reader= csv.DictReader(csvfile)
stateCode=list(state_code.state_codes.keys())
stateFullName=list(map(str.lower,state_code.states.values()))
countyName=list(map(str.lower,countyName))


US=state_code.US
weekCase=state_code.dict_for_regular_data['week case info']
weekDeath=state_code.dict_for_regular_data['week death info']
weekTest=state_code.dict_for_regular_data['test info']
weekHosp=state_code.dict_for_regular_data['Hosp info']
# weekComm=state_code.dict_for_regular_data['Comm info']


# D=defaultdict(list)



#   # Dictreader uses the first row as dictionary keys
# for l in reader:                 # each row is in the form {k1 : v1, ... kn : vn}
#     for k,v in l.items():  
#         D[k].append(v)  
# print(sys.getdefaultencoding())
# x=D['county']
# file = open('items.txt','w')
# for item in x:
# 	file.write('\"'+item+"\",")
# file.close()

# # print(D['county'])

app = FastAPI()

@app.get("/question/{Q}")

async def read_Q(Q):
    qtype=''
    doc = nlp(Q)
    gpe = []
    state=''
    county=''
    # key=[]
    flag=0
    vac=0
    ftype=0
    
    for stateName in stateCode:
        if stateName in Q:
            state=stateName
            
    for name in countyName:    
        x=Q.lower()   
        if(name in x) and (len(name)>len(county)):
                county=name 
    for ent in doc.ents:
        
        if (ent.label_ == 'GPE'):
            gpe.append(ent.text)
          
            
    for token in doc:
       
            
       if state=='':      
            if(token.text.lower() in stateFullName):
                state=state_code.us_state_to_abbrev[token.text.lower().capitalize()]
       if state=='' and county=='':
           if token.text in US:
               ftype=5
               qtype='us_status'
                         
    
    for word in state_code.dict_for_vac:
       
        if word in Q.lower(): 
            vac=1 
            break
        else : vac=0
        
    if vac==0 and ftype==0:
        if county=='':
            ftype=1
        else : ftype=2
    if vac==1 and ftype==0:
        if county=='':
            ftype=4
        else : ftype=3      
        
    # print(stateCode)
    # print(stateFullName)
    
    for word in weekCase:
        if word in Q.lower() and qtype=='' : 
           qtype='weekCase'
           break
       
    for word in weekDeath :
        if word in Q.lower() and qtype=='': 
           qtype='weekDeath'
           break
    for word in weekTest :
        if word in Q.lower() and qtype=='': 
           qtype='weekTest'
           break
    for word in weekTest :
        if word in Q.lower() and qtype=='': 
           qtype='testInfo'
           break
    for word in weekHosp :
        if word in Q.lower() and qtype=='': 
           qtype='HospInfo'
           break
    # +     
    print(qtype,ftype,vac)                                   
    result=getDataDetail(getDataFile(state,county,ftype),qtype,ftype,vac)       
    if result==None:
        result='No result'        
    
                
    return {"State name": state,'county name':county,'vac':vac,'result':result,'Q':Q.casefold(),'Gpe':gpe}
      
    
   

def getDataDetail(dic,qtype,ftype,vac):
   print(dic)
   if dic==None:
       result={'result':'null'}
       return result
   else:
    if qtype=='us_status':
        result={'US Total Cases':dic['us_total_cases'],'US Total Deaths':dic['us_total_deaths'],'Booster Pop Pct':dic['Bivalent_Booster_Pop_Pct']
                ,'us_trend_new_case':dic['us_trend_new_case'],'us_trend_new_death':dic['us_trend_new_death']
                }   
        return result
    if vac==1:
            if ftype==1: 
                result={'State':dic['StateName'],'At least 1 Dose':dic['At Least One Dose'],
                        'At Least One Dose rate of Total Population':dic['Administered_Dose1_Pop_Pct'],
                        'Completed Primary Series population':dic['Series_Complete_Yes'],
                        'Completed Primary Series rate':   dic["Series_Complete_Pop_Pct"]}
                return result
            
            if ftype==3: 
                
                result={'State':dic['StateName'],'County':dic['County'],'Completed Primary Series Population':dic['Series_Complete_Yes'],
                        'Completed Primary Series Population':dic['Series_Complete_Pop_Pct'],
                        'Completed Primary Series Rate':dic['Completeness_pct'],
                        'At Least One Dose Rate':dic['Administered_Dose1_Pop_Pct'],
                        'Booster Dose received population':dic['Booster_Doses']}
                
                return result 
    else:          
        
        if qtype=='weekCase':
            if ftype==1:
                result={'State':dic['StateName'],'New Case Last Week':dic['new_cases_past_7_days'],
                        'New Case Rate Last Week 100K':dic['Seven_day_cum_new_cases_per_100k']}
                return result
            if ftype==2:
                print(dic)
                result={'State':dic['State_name'],'County':dic['County'],'New Case Past 7 days':dic['Cases_7_day_count_change'],
                        'New Case Rate Past 7 days (100K)':dic['cases_per_100K_7_day_count_change'],
                        'New Case Rate changed from last week':dic['new_cases_week_over_week_percent_change'],
                        'Start Date':dic['positivity_start_date'],'End Date':dic['positivity_end_date']}
                return result
            
            
        if qtype=='weekDeath':
            
            if ftype==1:
                result={'State':dic['StateName'],'New Death Past 7 days':dic['new_deaths_past_7_days'],
                        '7 days Death rate in 100K':dic['seven_day_cum_new_deaths_per_100k']}
                return result
            if ftype==2:
                result={'State':dic['State_name'],'County':dic['County'],'New Death Past 7 days':dic['deaths_7_day_count_change'],
                        '7 days Death rate in 100K':dic['deaths_per_100K_7_day_count_change'],
                        '7 days Death Change from last week':dic['new_deaths_week_over_week_percent_change'],
                        'Start date':dic['case_death_start_date'],'End Date':dic['case_death_end_date']}
                return result
                
        if qtype=='testInfo':
                if ftype==1:
                    result={'State':dic['StateName'],'Postive ':dic['percent_positive_7_day_range'],
                            'Total Postive last week':dic['total_test_results_reported_7_day_count_change']
                            ,'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K']}
                    return result
                if ftype==2:
                    result={'State':dic['State_name'],'County':dic['County'],'Total Postive last week':dic['percent_test_results_reported_positive_last_7_days']
                            ,'Total Postive changed':dic['percent_test_results_reported_positive_last_7_days_7_day_count_change'],
                            'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K'],
                            'Postive Population rate in 100K changed':dic['total_new_test_results_reported_week_over_week_percent_change'],
                            'Start date':dic['testing_start_date'],'End date':dic['testing_end_date']}
                    return result
                    
        if qtype=='HospInfo':
            
            if ftype==1:   
                result={'State':dic['StateName'],'Pediatric adult number':dic['sum_previous_day_pediatric_and_adult_7DayAvg']}
                return result  
            
            if ftype==2:
                result={'State':dic['State_name'],'County':dic['County'],
                        'New Admissions last 7 days':dic['admissions_covid_confirmed_last_7_days'],
                        'New Admissions changed':dic['admissions_covid_confirmed_week_over_week_percent_change'],
                        'COVID Inpatient Beds Used':dic['percent_adult_inpatient_beds_used_confirmed_covid'],
                        'COVID Inpatient Beds Used changed from last week':dic['percent_adult_inpatient_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        'ICU Beds Used by Covid':dic['percent_adult_icu_beds_used_confirmed_covid'],
                        'ICU Beds Used by Covid changed from last week':dic['percent_adult_icu_beds_used_confirmed_covid_week_over_week_absolute_change']}
                return result
            
# if qtype=='CommInfo':
       
#    if qtype=='OverAll':                       
#        return dict(dic['statename'],dic['new_cases_07'],dic['date']) 
    
   