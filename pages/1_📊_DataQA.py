import streamlit as st
import requests, json
import pandas as pd
import altair as alt

def displayUS(result):
        st.write('')
        for k,v in result['result'].items():
            
            if k=='US_case_graph' :
                date=[]
                y=[]
                print(v)
                for x in v:
                    
                    y.append(x[0])
                    date.append(x[1])
                
                date=pd.to_datetime(date)  
                df = pd.DataFrame({'Number':y,'Date':date})

                print(df)
                
                c1 = alt.Chart(df,title='Case Trend(weekly)').mark_area(
                line={'color':'darkgreen'},
                color=alt.Gradient(
                        gradient='linear',
                        stops=[alt.GradientStop(color='white', offset=0),
                            alt.GradientStop(color='darkgreen', offset=1)],
                        x1=1,
                        x2=1,
                        y1=1,
                        y2=0
                    )
                    ).encode(alt.X("Date") , y= 'Number:Q' )
                            # st.line_chart(df,x='Date',y='Number',use_container_width=True)
                    # st.altair_chart(c)
                        # st.line_chart(df)
            if k=='US_death_graph' :
                date=[]
                y=[]
                
                for x in v:
                    date.append(x[1])
                    y.append(x[0])
                date=pd.to_datetime(date)  
                df = pd.DataFrame({'Number':y,'Date':date})

                print(df)
                
                c2 = alt.Chart(df,title='Death Trend (weekly)').mark_area(
                line={'color':'darkgreen'},
                color=alt.Gradient(
                        gradient='linear',
                        stops=[alt.GradientStop(color='white', offset=0),
                            alt.GradientStop(color='darkgreen', offset=1)],
                        x1=1,
                        x2=1,
                        y1=1,
                        y2=0
                    )
                    ).encode(alt.X("Date") , y= 'Number:Q' )
                            # st.line_chart(df,x='Date',y='Number',use_container_width=True)
                    # st.altair_chart(c)
                        # st.line_chart(df)    
            if k=='US_pediatric_graph' :
                date=[]
                y=[]
                
                for x in v:
                    date.append(x[1])
                    y.append(x[0])
                date=pd.to_datetime(date)  
                df = pd.DataFrame({'Number':y,'Date':date})

                print(df)
                
                c3 = alt.Chart(df,title='COVID Patient Confirmed (daily)' ).mark_area(
                line={'color':'darkgreen'},
                color=alt.Gradient(
                        gradient='linear',
                        stops=[alt.GradientStop(color='white', offset=0),
                            alt.GradientStop(color='Green', offset=1)],
                        x1=1,
                        x2=1,
                        y1=1,
                        y2=0
                    )
                    ).encode(alt.X("Date") , y= 'Number:Q' )
                            # st.line_chart(df,x='Date',y='Number',use_container_width=True)
                    # st.altair_chart(c)
                        # st.line_chart(df)
        col1, col2,col3,col4= st.columns(4) 
        col1.metric('US Total Cases',result['result']['US Total Cases'])  
        col2.metric('US Total Deaths',result['result']['US Total Deaths'])
        col3.metric('Admissions',result['result']['Admissions'])
        col4.metric('Booster',result['result']['Booster'])            
                        
        col1, col2 = st.columns([1, 3])
        col1.markdown('<h3>Case</h3>',unsafe_allow_html=True)
        col1.metric('US Total Cases',result['result']['US Total Cases'])
        col1.metric("US New Case", result['result']['us_trend_new_case'])                   
        st.text("")
        col2.altair_chart(c1)
        
        col1, col2 = st.columns([1, 3])
        col1.markdown('<h3>Death</h3> ',unsafe_allow_html=True)
        col1.metric('US Total Deaths',result['result']['US Total Deaths'])
        col1.metric("New Death", result['result']['us_trend_new_death'])                   
        st.text("")
        col2.altair_chart(c2)
        
        col1, col2 = st.columns([1, 3])
        col1.markdown('<h3>Hospitality</h3>',unsafe_allow_html=True)
        col1.metric('Admissions',result['result']['Admissions'])                 
        st.text("")
        col2.altair_chart(c3)
        st.markdown('<h3>Booster Dose Received Percent </h3>',unsafe_allow_html=True)
        BoosterPct=result['result']['Booster Pop Pct']
        
        Str='People with an Updated (Bivalent) Booster Dose:<h4>'+str(BoosterPct)+'%</h4>'
        st.markdown(Str,unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        col1.progress(BoosterPct/100)

st.set_page_config(
    
    page_title="Covid Data QA",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

# @st.cache_data # history
# def history(question):
#     his=[]
#     his.append(question)
#     return his
# def makeChart(Y,df,title):
#     chart = alt.Chart(df).mark_line().encode(
#                             x=alt.X('Date'),
#                             y=alt.Y(Y),
#                             ).properties(title=title)
#     st.altair_chart(chart, use_container_width=True)
col1, col2 = st.columns([4, 1])    
st.markdown('<h1 style="text-align: center">Covid Data QA</h1>', unsafe_allow_html=True)
st.markdown('<h3>Question</h3>', unsafe_allow_html=True)

question = st.text_input("Put your query", value="What are the new case in La Crosse WI",max_chars=50)
my_expander=st.expander(label='history',expanded=True)

button = st.button('Get Result')
headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

with st.sidebar:
    
    # st.markdown('<h2>Features Support</h2>', unsafe_allow_html=True)
    
    
    # st.markdown(''' - Covid New Case info''', unsafe_allow_html=True)
    # st.markdown(''' - Covid Death indo''', unsafe_allow_html=True)
    # st.markdown(''' - Covid Test info''', unsafe_allow_html=True)
    # st.markdown(''' - Covid Hospital info''', unsafe_allow_html=True)
    # st.markdown(''' - Covid Vaccine info''', unsafe_allow_html=True)
    
    st.markdown('<h2>How to ask</h3>', unsafe_allow_html=True)
    
    st.markdown(''' - County level info: Type the county name,state name(Abbr. works) and the feature you want to know, or skip it to get the overview''', unsafe_allow_html=True)
    st.markdown(''' - State level info: Type the state name(Abbr. works) and the feature you want to know, or skip it to get the overview''', unsafe_allow_html=True)
    st.markdown(''' - US level info: Well, just tpye 'US' should works''', unsafe_allow_html=True)
    st.markdown(''' - County/State Rank: Type Like 'Rank the county in WI',or'State rank'.''', unsafe_allow_html=True)
    st.markdown(''' - Try ZIP code?''', unsafe_allow_html=True)
    st.markdown(''' - State Abbr. has to be uppercase''', unsafe_allow_html=True)
    
    
# If the button is clicked or activated:
if button:
    

    # Set up the headers for the HTTP request. Here we specify that we accept JSON and we're sending JSON.
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    # Create the data payload for the request, which contains the question.
    data = {
         'question': question
    }
    if question=='':
        st.write('Please type in the question.')
    else:
    # Send an HTTP GET request to the specified URL, appending the question to the URL and providing the headers.
        response = requests.get('http://35.225.219.221:1145/question/'+question, headers=headers)
        
        # Parse the JSON response from the server and store the result.
        result = response.json()
        
        
        if result['code']==20:
            st.write('')
            st.markdown('<h3>'+result['result']+'</h3>', unsafe_allow_html=True)
        elif result['code']==0:
            displayUS(result)
        # st.write(result['result']['US Total Deaths'])
        # st.altair_chart(c2)
        # st.write(result['result']['Admissions'])
        # st.altair_chart(c3)
        # st.write(result['result']['Booster'])
        elif result['code']==8:
                df=pd.DataFrame(result['result'])
                df['New Case Past 7 days']=df['New Case Past 7 days'].astype('Int64')
                df=df.set_index('State')
                for (columnName, columnData) in df.items():
                    if df.dtypes[columnName]=='float64':
                        df[columnName]=df[columnName].round(decimals =2)
                df=df.sort_values(by=['New Case Past 7 days'],ascending=False)
                print(df.dtypes)        
                st.write(df)
                
        elif result['code']==9:
            
                df=pd.DataFrame(result['result'])
                df['New Case Past 7 days']=df['New Case Past 7 days'].astype('Int64')
                df=df.set_index('State')
                for (columnName, columnData) in df.items():
                    if df.dtypes[columnName]=='float64':
                        df[columnName]=df[columnName].round(decimals =2)
                df=df.sort_values(by=['New Case Past 7 days'],ascending=False)
                print(df.dtypes)        
                st.write(df)
                
        elif result['code']==7: # rank
                
                df=pd.DataFrame(result['result'])
                df['new_cases_07']=df['new_cases_07'].astype('Int64')
                df['new_deaths_07']=df['new_deaths_07'].astype('Int64')
                df['sum_previous_day_pediatric_and_adult_7DayAvg']=df['sum_previous_day_pediatric_and_adult_7DayAvg'].astype('float16')
                df['Series_Complete_12PlusPop_Pct']=df['Series_Complete_12PlusPop_Pct'].astype('float16')
                df['Series_Complete_5PlusPop_Pct']=df['Series_Complete_5PlusPop_Pct'].astype('float16')
                df=df.rename(columns={'state':'State','date':"Date",'statename':'State Full Name',"new_cases_07": "New Case last week", "new_deaths_07": "New Death last week",
                                'percent_positive_7_day_range':'Positivity','Series_Complete_12PlusPop_Pct':'Vaccine Series Completed Rate in Population over 12',
                                'Series_Complete_5PlusPop_Pct':'Vaccine Series Completed Rate in Population over 5'
                                })
                
                df=df.drop(labels="Date", axis=1)
                df=df.set_index('State')
                # for (columnName, columnData) in df.iteritems():
                #     if df.dtypes[columnName]=='float16':
                #         df[columnName]=df[columnName].round(decimals =2)
                
                print(df.dtypes)
                print(df)
                st.write(df.sort_values(by=['New Case last week'],ascending=False))
                
        elif(result['code']==6):
            
                    col1, col2 = st.columns(2)
                    if isinstance(result['result'], dict): 
                        i=1    
                        for k,v in result['result'].items():  
                            
                            
                            if i%2==1:
                                    col1.metric(k,v)
                            else: col2.metric(k,v)       
                            i=i+1
                        
        else:
                if type(result['result'])=='str':
                    st.markdown('<h3>'+result['result']+'</h3>', unsafe_allow_html=True)
                else:
                    tab1, tab2= st.tabs(["Current Data", "History Chart"])
                    
                    with tab1:
                        col1, col2 = st.columns(2)
                        if isinstance(result['result'], dict): 
                            i=1    
                            for k,v in result['result'].items():  
                                
                                
                                if i%2==1:
                                        col1.metric(k,v)
                                else: col2.metric(k,v)       
                                i=i+1
                            
                                
                        with tab2:
                            date=[]
                            case=[]
                            death=[]
                            test=[]
                            admission=[]
                            if(15>result['code']>=10):
                                st.write('Well, this part is no longer available')
                                # for x in result['History']: 
                                #         date.append(x['date'])
                                #         case.append(x['cases_7_day_count_change'])
                                #         death.append(x['deaths_7_day_count_change'])
                                #         test.append(x['new_test_results_reported_7_day_rolling_average'])
                                #         admission.append(x["admissions_covid_confirmed_last_7_days_per_100k_population"])
                                        
                                # date=pd.to_datetime(date)  
                                
                                # df = pd.DataFrame({'Case':case,'Date':date,'Death':death,'Test':test,'Admission':admission})
                            
                                
                                # df.sort_values(by='Date',ascending=True,inplace = True)
                                # df=df.reset_index(drop=True)
                                # print(type(df.Date[0]))
                                # print(df)
                                # max=len(df.index)
                                # min=0
                                # print(max)
                                
                                # if(result['code']==11 or result['code']==10):
                                    
                                #         chart = alt.Chart(df.iloc[min:max,:]).mark_line().encode(
                                #         x=alt.X('Date'),
                                #         y=alt.Y('Case:Q'),
                                #         ).properties(title='Case History')
                                #         # values = st.slider(
                                #         # 'Select a range ',
                                #         # 0, max, (0, max))
                                #         # st.write('Values:', values)
                                #         st.altair_chart(chart, use_container_width=True)
                                #         # min=values[0]
                                #         # max=values[1]
                                #         # k=k+1

                                    
                                # if(result['code']==12 or result['code']==10):   
                                #     chart = alt.Chart(df).mark_line().encode(
                                #     x=alt.X('Date'),
                                #     y=alt.Y('Death:Q'),
                                #     ).properties(title="Death History")
                                #     st.altair_chart(chart, use_container_width=True)
                                    
                                # if(result['code']==13 or result['code']==10):
                                #     chart = alt.Chart(df).mark_line().encode(
                                #     x=alt.X('Date'),
                                #     y=alt.Y('Test:Q'),
                                #     ).properties(title="Test History")
                                #     st.altair_chart(chart, use_container_width=True)
                                    
                                # if(result['code']==14 or result['code']==10):    
                                    
                                #     chart = alt.Chart(df).mark_line().encode(
                                #     x=alt.X('Date'),
                                #     y=alt.Y('Admission:Q'),
                                #     ).properties(title="Admission History")
                                #     st.altair_chart(chart, use_container_width=True)
                                    
                            if(result['code']<10):
                                st.write('Well, this part is no longer available')
                            # for x in result['History']: 
                            #         date.append(x['submission_date'])
                            #         case.append(x['new_case'])
                            #         death.append(x['new_death'])
                            #         test.append(x['new_test_results_reported_7_day_rolling_average'])
                                    
                            # date=pd.to_datetime(date)
                            # df = pd.DataFrame({'Case':case,'Date':date,'Death':death,'Test':test})
                            # df=df.dropna()
                            # if(result['code']==2 or result['code']==1):
                            #     chart = alt.Chart(df).mark_line().encode(
                            #     x=alt.X('Date'),
                            #     y=alt.Y('Case:Q'),
                            #     ).properties(title="Case History")
                            #     st.altair_chart(chart, use_container_width=True)
                                
                            # if(result['code']==3 or result['code']==1):   
                            #     chart = alt.Chart(df).mark_line().encode(
                            #     x=alt.X('Date'),
                            #     y=alt.Y('Death:Q'),
                            #     ).properties(title="Death History")
                            #     st.altair_chart(chart, use_container_width=True)
                            # if(result['code']==4 or result['code']==1):
                            #     chart = alt.Chart(df).mark_line().encode(
                            #     x=alt.X('Date'),
                            #     y=alt.Y('Test:Q'),
                            #     ).properties(title="Test History")
                            #     st.altair_chart(chart, use_container_width=True)
    #             with tab3:
    #                 st.write('''For the county level data, you just need to type the county name and the state name(capital abbr. works), 
    # then it will return you the latest statistics(usually last week's). Same to State level. Currently we support five main features based on our data source,
    # Case,Death,Test,Hospital and Vaccine. You can also refine your question with the feature you want to know ,then it will 
    # just return that feature's info, like 'How many new case in new york city last week'. You might find some of data displayed as 'suppressed'(usually Death info),
    # that just because the loacl offical stop to collect that part of data, I can't help with this. You can also take a glance of 
    # all the states' Covid statistics in a table form by type something like 'State rank'. County table works in the same way, like 
    # 'Rank in NY'. If you want to take a look of the US Covid dashboard, try 'US'.
    # For the people too lazy to type a word, just input a zip code,yea we support that.
    # ''')

                        
                          
            