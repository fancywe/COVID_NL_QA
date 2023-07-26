# Libraries
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Covid NL QA', page_icon='random', layout='centered')

# Title
st.title('🦠 Covid QA 🧫')

st.write(
    
    """
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    This project, conceived and executed individually, aims to provide answers to queries related to Covid-19, encompassing both statistical data and scientific literature. At the inception of this project, the Covid-19 pandemic was a pressing issue globally. However, as the project progressed, the significance of the pandemic declined, rendering it largely irrelevant.

Indeed, by 2022, the upkeep of most Covid-19 related APIs and databases ceased due to the subsiding importance of the pandemic. Despite these challenges and dwindling resources, I have successfully brought this project to fruition, although the results might not be as comprehensive as initially envisioned.
    """
)

st.subheader('DataQA')
st.write(
    """
    This is the major portion of my project involved developing an API that can handle natural language inputs. This API undergoes a word frequency analysis process to predict the type of question being asked and subsequently returns the corresponding results. It is important to note that the accuracy of this prediction is less than ideal, largely due to the limitations of the training data, which was manually curated and somewhat sparse.

The data source for this segment of the project was obtained from the official Covid tracker provided by the Centers for Disease Control and Prevention (CDC). Although the CDC does not provide a public API, I managed to script a solution that allowed me to gather data daily. Nonetheless, the inherent update period for the data is typically one week.
    """
)
st.subheader('PaperQA')
st.write(
    """
    The second component of the project can be considered an extension of an existing project, with a pretrained machine learning model. However, the model's accuracy remains sub-optimal. A primary challenge encountered in this module was the cessation of updates for our data source, The COVID-19 Open Research Dataset. Despite extensive search, an adequate alternative could not be identified, which led to the decision to temporarily suspend this module. As such, this module is presently offline.
    """
)