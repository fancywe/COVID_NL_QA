import streamlit as st
import requests, json
import pandas as pd
import altair as alt

st.set_page_config(
    
    page_title="Covid QA",
    page_icon="🧊",
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
st.markdown('<h1 style="text-align: center">Covid QA</h1>', unsafe_allow_html=True)
st.markdown('<h3>Question</h3>', unsafe_allow_html=True)

question = st.text_input("Put your query", value="What are the new case in La Crosse WI")
my_expander=st.expander(label='history',expanded=True)

# for q in his:
#         st.write(q)
#         st.write('123')
button = st.button('Get Result')

with st.sidebar:
    st.markdown('<h1>COVID info QA</h3>', unsafe_allow_html=True)
    add_radio = st.radio(
        "Navigation",
        ("COVID Statistics Data QA", "COVID Thesis QA")
    )
    st.markdown('<h3>About</h3>', unsafe_allow_html=True)
    st.text('')

if button:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
         'question': question
    }
    response = requests.get('http://127.0.0.1:8000/question/'+question, headers=headers)
    result = response.json()
    # history(question)

    # print(result)
    if result['code']==20:
        st.write(result['result'])
    elif result['code']==0:
          
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
            for (columnName, columnData) in df.iteritems():
                if df.dtypes[columnName]=='float16':
                    df[columnName]=df[columnName].round(decimals =2)
            
            print(df.dtypes)
            print(df)
            st.write(df.sort_values(by=['New Case last week'],ascending=False))
            
    elif(result['code']==6):
           
                col1, col2 = st.columns(2)
                if isinstance(result['result'], dict): 
                    # result['result']
                    key=''
                    value=0
                    last=0
                    i=0  
                    
                    for k,v in result['result'].items():  
                        if k=='History':
                            break
                        if 'changed' in k:
                            last=v
                        else:
                            if k=='State':
                                col1.metric(k,v)
                                
                            elif last!=0:
                                if i%2==1:
                                    col1.metric(key,value,last) 
                                    key=k
                                    value=v 
                                    last=0
                                else:
                                    col1.metric(key,value,last) 
                                    key=k
                                    value=v 
                                    last=0
                            elif key!='':
                                if i%2==1:
                                    col1.metric(key,value)
                                    key=k
                                    value=v
                                else:
                                    col2.metric(key,value)
                                    key=k
                                    value=v
                            else:
                                    key=k
                                    value=v
                        i=i+1
                    if i%2==1:       
                        col1.metric(key,value) 
                    else:
                        col2.metric(key,value) 
    else:
            tab1, tab2 = st.tabs(["Current Data", "History Chart"])
            
            with tab1:
                col1, col2 = st.columns(2)
                if isinstance(result['result'], dict): 
                    # result['result']
                    key=''
                    value=0
                    last=0
                    i=0  
                    start=''
                    end=''
                    for k,v in result['result'].items():  
                        i=i+1
                        if 'changed' in k:
                            last=v
                        else:
                            if k=='State':
                                col1.metric(k,v)
                                
                                
                            elif last!=0:
                                if i%2==1:
                                    col1.metric(key,value,last) 
                                    key=k
                                    value=v 
                                    last=0
                                else:
                                    col1.metric(key,value,last) 
                                    key=k
                                    value=v 
                                    last=0
                            elif key!='':
                                if i%2==1:
                                    col1.metric(key,value)
                                    key=k
                                    value=v
                                else:
                                    col2.metric(key,value)
                                    key=k
                                    value=v
                            else:
                                    key=k
                                    value=v
                       
                    if i%2==1:       
                        col1.metric(key,value) 
                    else:
                        col2.metric(key,value)
                    
                        
                with tab2:
                    date=[]
                    case=[]
                    death=[]
                    test=[]
                    admission=[]
                    if(15>result['code']>=10):
                        for x in result['History']: 
                                date.append(x['date'])
                                case.append(x['cases_7_day_count_change'])
                                death.append(x['deaths_7_day_count_change'])
                                test.append(x['new_test_results_reported_7_day_rolling_average'])
                                admission.append(x["admissions_covid_confirmed_last_7_days_per_100k_population"])
                                
                        date=pd.to_datetime(date)  
                        
                        df = pd.DataFrame({'Case':case,'Date':date,'Death':death,'Test':test,'Admission':admission})
                    
                        # d 
                        df.sort_values(by='Date',ascending=True,inplace = True)
                        df=df.reset_index(drop=True)
                        print(type(df.Date[0]))
                        print(df)
                        max=len(df.index)
                        min=0
                        print(max)
                        
                        if(result['code']==11 or result['code']==10):
                            
                                chart = alt.Chart(df.iloc[min:max,:]).mark_line().encode(
                                x=alt.X('Date'),
                                y=alt.Y('Case:Q'),
                                ).properties(title='Case History')
                                values = st.slider(
                                'Select a range ',
                                0, max, (0, max))
                                # st.write('Values:', values)
                                st.altair_chart(chart, use_container_width=True)
                                # min=values[0]
                                # max=values[1]
                                # k=k+1

                            
                        if(result['code']==12 or result['code']==10):   
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Death:Q'),
                            ).properties(title="Death History")
                            st.altair_chart(chart, use_container_width=True)
                            
                        if(result['code']==13 or result['code']==10):
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Test:Q'),
                            ).properties(title="Test History")
                            st.altair_chart(chart, use_container_width=True)
                            
                        if(result['code']==14 or result['code']==10):    
                            
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Admission:Q'),
                            ).properties(title="Admission History")
                            st.altair_chart(chart, use_container_width=True)
                            
                    if(result['code']<10):
                        
                        for x in result['History']: 
                                date.append(x['submission_date'])
                                case.append(x['new_case'])
                                death.append(x['new_death'])
                                test.append(x['new_test_results_reported_7_day_rolling_average'])
                                
                        date=pd.to_datetime(date)
                        df = pd.DataFrame({'Case':case,'Date':date,'Death':death,'Test':test})
                        df=df.dropna()
                        if(result['code']==2 or result['code']==1):
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Case:Q'),
                            ).properties(title="Case History")
                            st.altair_chart(chart, use_container_width=True)
                            
                        if(result['code']==3 or result['code']==1):   
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Death:Q'),
                            ).properties(title="Death History")
                            st.altair_chart(chart, use_container_width=True)
                        if(result['code']==4 or result['code']==1):
                            chart = alt.Chart(df).mark_line().encode(
                            x=alt.X('Date'),
                            y=alt.Y('Test:Q'),
                            ).properties(title="Test History")
                            st.altair_chart(chart, use_container_width=True)
                        
                          
            