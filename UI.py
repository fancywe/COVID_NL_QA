import streamlit as st
import requests, json

st.set_page_config(
    
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


question = st.text_input("Put your query", value="What are the new case in La Crosse WI")
button = st.button('Get Result')
st.text("")
st.text("")
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

    print(result)
    x=len(result)
    print(x)
    for k,v in result['result'].items():
        st.metric(label=k, value=v)
    st.write(x)