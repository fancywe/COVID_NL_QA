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
import zipcodes
from Q_handler import Handle
#import jamspell
import unittest

from spellchecker import SpellChecker

from fastapi import FastAPI

from county_code import countyName

weekCase=state_code.dict_for_regular_data['week case info']
weekDeath=state_code.dict_for_regular_data['week death info']
weekTest=state_code.dict_for_regular_data['test info']
weekHosp=state_code.dict_for_regular_data['Hosp info']

stateCode=list(state_code.state_codes.keys())
stateFullName=list(map(str.lower,state_code.states.values()))
countyName=list(map(str.lower,countyName))
vac=state_code.dict_for_vac

#Load trained pipeline for English
nlp =spacy.load('en_core_web_sm')
#Instantiate FastAPI
app = FastAPI()
#Receives HTTP requests in this paths, Q as the user input
@app.get("/question/{Q}")

#Function to process question
def read_Q(Q):
        
    #Process the question text  
    doc = nlp(Q) 
    #Initialize variables
    gpe = []     
    state=''
    county=''
    code=0
    history=None
    us=0
    #Instantiate SpellChecker
    spell = SpellChecker()
    #Load the whitelist (proper noun)
    spell.word_frequency.load_text_file('Counties name.txt') 
    #Check if it is a zip code query 
    if Q=='US': us=1                                      
    if Q.isdigit():
        if len(Q)==5:
            if zipcodes.is_real(Q): #if zip code is valid, record the state name and the county name
                county=zipcodes.matching(Q)[0]['city'].lower()
                state=zipcodes.matching(Q)[0]['state']
                code=10
            else:
                result='This is not a valid zip code'     
        else:
            result='This is not a valid zip code' 
    else:       
        
        for stateName in stateCode:
                if stateName in Q:
                        state=stateName
                        
        for stateName in stateFullName:
                if state=='':      
                        if(stateName in Q.lower()):
                                state=state_code.us_state_to_abbrev[stateName.capitalize()] 
        # Q=''                        
        # for token in doc:
        #         Q=Q+spell.correction(token.text)+' '
        #         print(Q)
                
        for ent in doc.ents:
                print(doc.ents)
                if (ent.label_ == 'GPE'):
                        gpe.append(ent.text)
        for name in countyName:    
                x=Q.lower()   
                if(name in x) and (len(name)>len(county)):
                        county=name 
                        
        for stateName in stateFullName:
                if state=='':      
                        if(stateName in Q.lower()):
                                state=state_code.us_state_to_abbrev[stateName.capitalize()]                             
                
        # for stateName in stateCode:
        #         if stateName in Q:
        #                 state=stateName

        

                        
        # for word in weekCase:
        #         if word in Q.lower():
        #                 Q+=' case'
        #                 key=1
        #                 break
        # for word in weekDeath :
        #         if word in Q.lower(): 
        #                 Q+=' death'
        #                 key=1
        #                 break
        # for word in weekTest :
        #         if word in Q.lower() : 
        #                 Q+=' test'
        #                 key=1
        #                 break
        # for word in vac :
        #         if word in Q.lower(): 
        #                 Q+=' vac'
        #                 key=1
        #                 break
        # for word in weekHosp :
        #         if word in Q.lower() : 
        #                 Q+='hosp'
        #                 key=1
        #                 break        
        # if state!='':
        #         Q+=' state'
        #         geo=1
        # if county!='':
        #         Q+=' county' 
        #         geo=1
    rank=0
    if 'rank' in Q:
            rank=1               
    if len(gpe)==0 and state=='' and county=='' and rank==0:
        code=20
        result='No place detected'
    if state=='' and county!='' and rank==0:
        print(county)
        code=20
        result='Please input State name'     
               
    elif code==0:
            if us==1:
                result=getDataDetail(getDataFile(state,county,code),code)
            else:
                if state=='': x=1
                else: x=0
                if county=='': y=1
                else: y=0
                #Pass the preprocessed question text to the ML model
                code=Handle(Q,x,y).item()
                #Print the predict result
                print('ML model predict result: ',code)
                #Print the place name in the question (for test)
                # print('Place name in the question: ',gpe) 
                
                                                          
                result=getDataDetail(getDataFile(state,county,code),code)
                print(result)
                # if 'History' in result:
                #         history=result.pop("History", None)  
                #         print(result)    
    if result==None:
        result='No query result found'        
    
                
    return {"State name": state,'County name':county,'code':code,'result':result,'Q':Q.casefold(),'History':history,'Gpe':gpe}
      
    
   

def getDataDetail(dic,code):
   
   if dic==None:
       result={'result':'null'}
       return result
   else:
    if code==0:
        result={'US Total Cases':dic['us_total_cases'],'US Total Deaths':dic['us_total_deaths'],'Booster Pop Pct':dic['Bivalent_Booster_Pop_Pct']
                ,'us_trend_new_case':dic['us_trend_new_case'],'us_trend_new_death':dic['us_trend_new_death'],'US_case_graph':dic['new_case'],
                'US_death_graph':dic['new_death'],'US_pediatric_graph':dic['sum_previous_day_pediatric_and_adult_7DayAvg'],
                'Booster':dic['Bivalent_Booster'],'Admissions':dic['sum_inpatient_beds_used_clean']
                }   
        return result
    elif code==6:
            
                result={'State':dic['StateName'],'At least 1 Dose Population':dic['Administered_Dose1_Recip'],
                        'At Least One Dose rate of Total Population':dic['Administered_Dose1_Pop_Pct'],
                        'Completed Primary Series Population':dic['Series_Complete_Yes'],
                        'Completed Primary Series Rate':   dic["Series_Complete_Pop_Pct"],
                        'Booster Received':dic['Bivalent_Booster'],'Booster Received Rate':dic['Bivalent_Booster_Pop_Pct']}
                return result
            
    elif code==15: 
                
                result={'State':dic['StateName'],'County':dic['County'],'Completed Primary Series Population':dic['Series_Complete_Yes'],
                        'Completed Primary Series Population':dic['Series_Complete_Pop_Pct'],
                        'Completed Primary Series Rate':dic['Completeness_pct'],
                        'At Least One Dose Rate':dic['Administered_Dose1_Pop_Pct'],
                        'Booster Dose received population':dic['Booster_Doses']}
                
                return result 
    elif code==7:
                result=dic
                return dic
    elif code==9:
                result=dic
                return dic
    elif code==8:
                result=dic
                print(dic)
                print(type(dic))
                return dic 
    elif code==16:
                result=dic
                print(dic)
                print(type(dic))
                return dic                 
        
    elif code==1:
                result={'State':dic['StateName'],'New Case Last Week':dic['new_cases_past_7_days'],
                        'New Case Rate Last Week 100K':dic['Seven_day_cum_new_cases_per_100k']
                        ,'New Death Past 7 days':dic['new_deaths_past_7_days'],
                        '7 days Death rate in 100K':dic['seven_day_cum_new_deaths_per_100k'],
                        'Total Postive last week':dic['total_test_results_reported_7_day_count_change']
                        ,'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K'],
                        'Pediatric adult number':dic['sum_previous_day_pediatric_and_adult_7DayAvg'],'At least 1 Dose Population':dic['Administered_Dose1_Recip'],
                        'At Least One Dose rate of Total Population':dic['Administered_Dose1_Pop_Pct'],
                        'Completed Primary Series Population':dic['Series_Complete_Yes'],
                        'Completed Primary Series Rate':   dic["Series_Complete_Pop_Pct"],
                        'Booster Received':dic['Bivalent_Booster'],'Booster Received Rate':dic['Bivalent_Booster_Pop_Pct']
                        # ,'History':dic['History']
                        }
                return result

    elif code==10:
                
                result={'State':dic['State_name'],'County':dic['County'],'Level':dic['CCL_community_burden_level'],'New Case Past 7 days':dic['Cases_7_day_count_change'],
                        'New Case Rate Past 7 days (100K)':dic['cases_per_100K_7_day_count_change'],
                        'New Case Rate changed':dic['new_cases_week_over_week_percent_change'],
                        'New Death Past 7 days':dic['deaths_7_day_count_change'],
                        '7 days Death rate in 100K':dic['deaths_per_100K_7_day_count_change'],
                        '7 days Death changed ':dic['new_deaths_week_over_week_percent_change'],
                        'Total Postive last week':dic['percent_test_results_reported_positive_last_7_days']
                        ,'Total Postive changed':dic['percent_test_results_reported_positive_last_7_days_7_day_count_change'],
                        'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K'],
                        'Postive Population rate in 100K changed':dic['total_new_test_results_reported_week_over_week_percent_change'],
                        'New Admissions last 7 days':dic['admissions_covid_confirmed_last_7_days'],
                        'New Admissions changed':dic['admissions_covid_confirmed_week_over_week_percent_change'],
                        'COVID Inpatient Beds Used':dic['percent_adult_inpatient_beds_used_confirmed_covid'],
                        'COVID Inpatient Beds Used changed':dic['percent_adult_inpatient_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        'ICU Beds Used by Covid':dic['percent_adult_icu_beds_used_confirmed_covid'],
                        'ICU Beds Used by Covid changed':dic['percent_adult_icu_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        # 'History':dic['History']
                        # ,'Completed Primary Series Population':dic['Series_Complete_Yes'],
                        # 'Completed Primary Series Population':dic['Series_Complete_Pop_Pct'],
                        # 'Completed Primary Series Rate':dic['Completeness_pct'],
                        # 'At Least One Dose Rate':dic['Administered_Dose1_Pop_Pct'],
                        # 'Booster Dose received population':dic['Booster_Doses']    
                        }
                return result
            
       
    elif code==2:
                result={'State':dic['StateName'],'New Case Last Week':dic['new_cases_past_7_days'],
                        'New Case Rate Last Week 100K':dic['Seven_day_cum_new_cases_per_100k']
                        # ,'History':dic['History']
                        }
                return result
    elif code==11:
                
                result={'State':dic['State_name'],'County':dic['County'],'Level':dic['CCL_community_burden_level'].capitalize(),'New Case Past 7 days':dic['Cases_7_day_count_change'],
                        'New Case Rate Past 7 days (100K)':dic['cases_per_100K_7_day_count_change'],
                        'New Case Rate changed':dic['new_cases_week_over_week_percent_change'],
                        'Start Date':dic['positivity_start_date'],'End Date':dic['positivity_end_date']}
                return result
            
            
    elif code==3:
            
            
                result={'State':dic['StateName'],'New Death Past 7 days':dic['new_deaths_past_7_days'],
                        '7 days Death rate in 100K':dic['seven_day_cum_new_deaths_per_100k']
                        #,'History':dic['History']
                        }
                return result
    elif code==12:
                result={'State':dic['State_name'],'County':dic['County'],'Level':dic['CCL_community_burden_level'].capitalize(),'New Death Past 7 days':dic['deaths_7_day_count_change'],
                        '7 days Death rate in 100K':dic['deaths_per_100K_7_day_count_change'],
                        '7 days Death change from last week':dic['new_deaths_week_over_week_percent_change'],
                        'Start date':dic['case_death_start_date'],'End Date':dic['case_death_end_date']
                        #,'History':dic['History']
                        }
                return result
                
    elif code==4:
                
                
                    result={'State':dic['StateName'],'Postive ':dic['percent_positive_7_day_range'],
                            'Total Postive last week':dic['total_test_results_reported_7_day_count_change']
                            ,'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K']
                        #     ,'History':dic['History']
                            }
                    
                    return result
    elif code==13:
                    result={'State':dic['State_name'],'County':dic['County'],'Level':dic['CCL_community_burden_level'].capitalize(),'Total Postive last week':dic['percent_test_results_reported_positive_last_7_days']
                            ,'Total Postive changed':dic['percent_test_results_reported_positive_last_7_days_7_day_count_change'],
                            'Postive Population rate in 100K':dic['total_test_results_reported_7_day_count_change_per_100K'],
                            'Postive Population rate in 100K changed':dic['total_new_test_results_reported_week_over_week_percent_change'],
                            'Start date':dic['testing_start_date'],'End date':dic['testing_end_date']}
                    
                    return result
                    
    elif code==5:
            
                result={'State':dic['StateName'],'Pediatric adult number':dic['sum_previous_day_pediatric_and_adult_7DayAvg']}
                return result  
            
    elif code==14:
                result={'State':dic['State_name'],'County':dic['County'],'Level':dic['CCL_community_burden_level'].capitalize(),
                        'New Admissions last 7 days':dic['admissions_covid_confirmed_last_7_days'],
                        'New Admissions changed':dic['admissions_covid_confirmed_week_over_week_percent_change'],
                        'COVID Inpatient Beds Used':dic['percent_adult_inpatient_beds_used_confirmed_covid'],
                        'COVID Inpatient Beds Used changed':dic['percent_adult_inpatient_beds_used_confirmed_covid_week_over_week_absolute_change'],
                        'ICU Beds Used by Covid':dic['percent_adult_icu_beds_used_confirmed_covid'],
                        'ICU Beds Used by Covid changed':dic['percent_adult_icu_beds_used_confirmed_covid_week_over_week_absolute_change']
                        
                        }
                return result
            
# if qtype=='CommInfo':
       
#    if qtype=='OverAll':                       
#        return dict(dic['statename'],dic['new_cases_07'],dic['date']) 
    
   