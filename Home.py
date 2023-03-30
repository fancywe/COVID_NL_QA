# Libraries
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Covid NL QA', page_icon='random', layout='centered')

# Title
st.title('🦠 Covid QA 🧫')

st.write(
    
    """
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    This is a small individual project to answer Covid related question(Statistics / Papers). 
    By the time I start this project, Covid was still a pretty big issue and now it just something irrelevant.
    Actually most of Covid related API and database stop maintenance in 2022, but I still managed to get this project done(well, not that good tho)
    """
)

st.subheader('DataQA')
st.write(
    """
    This part take the majority of my workload, I maintained a API that accept natural language as input and after a word frequency analysis process
    it will predicts the type of the question then return the corresponding result. Notice that the prediction accuracy is not very ideal, 
    which blame to the training data which is totally handwrited and insufficient in quantity. The data source of this part is from 
    [CDC(Centers for Disease Control and Prevention) offical Covid tracker](https://covid.cdc.gov/covid-data-tracker/#datatracker-home), they don't really provid a public API, 
    I used some kind of script thing to obtain data everyday,well the update period of the data itself is usually one week though.  
    """
)
st.subheader('PaperQA')
st.write(
    """
    Well this part is more like a plug-in of an existing project, the ML model is from someone else (well it is also not that accurate LOL)
    But the main issue of this part is the datasource [The COVID-19 Open Research Dataset](https://github.com/allenai/cord19) is completely stopped updating,
    and I didn't find appropriate substitute, so I just leave it there.
    """
)