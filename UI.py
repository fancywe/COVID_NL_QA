import streamlit as st
import requests, json
import pandas as pd
import altair as alt

st.set_page_config(
    
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown('<h1 style="text-align: center">Covid QA</h1>', unsafe_allow_html=True)
st.markdown('<h3>Question</h3>', unsafe_allow_html=True)
question = st.text_input("Put your query", value="What are the new case in La Crosse WI")
button = st.button('Get Result')
st.text("")

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

    # print(result)
    
    if result['code']==1:
        
        
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
    else:
        print(result)
        print(type(result['result']))
        
        if isinstance(result['result'], dict): 
            key=''
            value=0
            last=0  
            for k,v in result['result'].items():  
                
                if 'changed' in k:
                    last=v
                else:
                    if last!=0:
                        st.metric(key,value,last) 
                        key=k
                        value=v 
                        last=0
                    elif key!='':
                        st.metric(key,value)
                        key=k
                        value=v
                    else:
                        key=k
                        value=v
                        
            st.metric(key,value)            
        elif isinstance(result['result'], list):
            df=pd.DataFrame(result['result'])
            st.write(df)