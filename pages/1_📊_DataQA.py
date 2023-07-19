import streamlit as st
import requests, json
import pandas as pd
import altair as alt
from matplotlib import pyplot as plt

import seaborn as sns
import matplotlib.style as style
from datetime import date
import matplotlib.dates as dates
from matplotlib.dates import MonthLocator, DateFormatter, WeekdayLocator
from matplotlib.ticker import NullFormatter
import seaborn as sns
from urllib.request import urlopen
import json 
import pandas as pd
import requests
from matplotlib.figure import Figure


st.set_page_config(
    
    page_title="Covid Data QA",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)


today = date.today()
#sns.set_style('whitegrid')
style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
#plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 10, 10

# import matplotlib as mpl
# mpl.use("agg")

from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock

@st.cache(ttl=3*60*60, suppress_st_warning=True)
def get_data():
    US_confirmed = 'json/US.csv'
    US_deaths = 'json/death.csv'
    confirmed = pd.read_csv(US_confirmed)
    deaths = pd.read_csv(US_deaths)
    # print(confirmed)
    # print(deaths)
    return confirmed, deaths

confirmed, deaths = get_data()

def plot_state(state):
    import numpy as np
    #FIPSs = confirmed.groupby(['Province_State', 'Admin2']).FIPS.unique().apply(pd.Series).reset_index()
    #FIPSs.columns = ['State', 'County', 'FIPS']
    #FIPSs['FIPS'].fillna(0, inplace = True)
    #FIPSs['FIPS'] = FIPSs.FIPS.astype(int).astype(str).str.zfill(5)
    @st.cache(ttl=3*60*60, suppress_st_warning=True)
    def get_testing_data_state():
            apiKey = 'e7c0018658814e29b12b1286bfd83ae9'
            st.text('Getting testing data for California State')
            path1 = 'https://data.covidactnow.org/latest/us/states/'+state+'.OBSERVED_INTERVENTION.timeseries.json?apiKey='+apiKey
            df = json.loads(requests.get(path1).text)
            data = pd.DataFrame.from_dict(df['actualsTimeseries'])
            data['Date'] = pd.to_datetime(data['date'])
            data = data.set_index('Date')
            
            try:
                data['new_negative_tests'] = data['cumulativeNegativeTests'].diff()
                data.loc[(data['new_negative_tests'] < 0)] = np.nan
            except: 
                data['new_negative_tests'] = np.nan
                print('Negative test data not avilable')
            data['new_negative_tests_rolling'] = data['new_negative_tests'].fillna(0).rolling(14).mean()
            
            
            try:
                data['new_positive_tests'] = data['cumulativePositiveTests'].diff()
                data.loc[(data['new_positive_tests'] < 0)] = np.nan
            except: 
                data['new_positive_tests'] = np.nan
                st.text('test data not avilable')
            data['new_positive_tests_rolling'] = data['new_positive_tests'].fillna(0).rolling(14).mean()
            data['new_tests'] = data['new_negative_tests']+data['new_positive_tests']
            data['new_tests_rolling'] = data['new_tests'].fillna(0).rolling(14).mean()
            data['testing_positivity_rolling'] = (data['new_positive_tests_rolling'] / data['new_tests_rolling'])*100
            return data['new_tests_rolling'], data['testing_positivity_rolling'].iloc[-1:].values[0]
            
    
    testing_df, testing_percent = get_testing_data_state()
    county_confirmed = confirmed[confirmed.Province_State == 'California']
    #county_confirmed = confirmed[confirmed.Admin2 == county]
    county_confirmed_time = county_confirmed.drop(county_confirmed.iloc[:, 0:12], axis=1).T #inplace=True, axis=1
    county_confirmed_time = county_confirmed_time.sum(axis= 1)
    county_confirmed_time = county_confirmed_time.reset_index()
    county_confirmed_time.columns = ['date', 'cases']
    county_confirmed_time['Datetime'] = pd.to_datetime(county_confirmed_time['date'])
    county_confirmed_time = county_confirmed_time.set_index('Datetime')
    del county_confirmed_time['date']
    #print(county_confirmed_time.head())
    incidence= pd.DataFrame(county_confirmed_time.cases.diff())
    incidence.columns = ['incidence']
    
    #temp_df_time = temp_df.drop(['date'], axis=0).T #inplace=True, axis=1
    county_deaths = deaths[deaths.Province_State == 'California']
    population = county_deaths.Population.values.sum()
    
    del county_deaths['Population']
    county_deaths_time = county_deaths.drop(county_deaths.iloc[:, 0:11], axis=1).T #inplace=True, axis=1
    county_deaths_time = county_deaths_time.sum(axis= 1)
    
    county_deaths_time = county_deaths_time.reset_index()
    county_deaths_time.columns = ['date', 'deaths']
    county_deaths_time['Datetime'] = pd.to_datetime(county_deaths_time['date'])
    county_deaths_time = county_deaths_time.set_index('Datetime')
    del county_deaths_time['date']
    
    cases_per100k  = ((county_confirmed_time)*100000/population)
    cases_per100k.columns = ['cases per 100K']
    cases_per100k['rolling average'] = cases_per100k['cases per 100K'].rolling(7).mean()
    
    deaths_per100k  = ((county_deaths_time)*100000/population)
    deaths_per100k.columns = ['deaths per 100K']
    deaths_per100k['rolling average'] = deaths_per100k['deaths per 100K'].rolling(7).mean()
    
    
    incidence['rolling_incidence'] = incidence.incidence.rolling(7).mean()
    metric = (incidence['rolling_incidence']*100000/population).iloc[[-1]]
    st.text('Number of new cases averaged over last seven days = %s' %'{:,.1f}'.format(metric.values[0]))
    st.text("Population under consideration = %s"% '{:,.0f}'.format(population))
    st.text("Total cases = %s"% '{:,.0f}'.format(county_confirmed_time.tail(1).values[0][0]))
    st.text("Total deaths = %s"% '{:,.0f}'.format(county_deaths_time.tail(1).values[0][0]))
    st.text("% test positivity (14 day average)= "+"%.2f" % testing_percent)
    #print(county_deaths_time.tail(1).values[0])
    #print(cases_per100k.head())
    fig = Figure(figsize=(12,8))
    #fig, ((ax4, ax3),(ax1, ax2)) = plt.subplots(2,2, figsize=(6,4))
    ((ax4, ax3),(ax1, ax2)) = fig.subplots(2,2)
    
    county_confirmed_time.plot(ax = ax1,  lw=4, color = '#377eb8')
    county_deaths_time.plot(ax = ax1,  lw=4, color = '#e41a1c')
    ax1.set_xlabel('Time') 
    ax1.set_ylabel('Number of individuals')
    
    
    
    testing_df.plot(ax = ax2,  lw=4, color = '#377eb8')
    #cases_per100k['cases per 100K'].plot(ax = ax2,  lw=4, linestyle='--', color = '#377eb8')
    #cases_per100k['rolling average'].plot(ax = ax2, lw=4, color = '#377eb8')
    
    #deaths_per100k['deaths per 100K'].plot(ax = ax2,  lw=4, linestyle='--', color = '#e41a1c')
    #deaths_per100k['rolling average'].plot(ax = ax2, lw=4, color = '#e41a1c')
    
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Number of new tests')
    
    incidence.incidence.plot(kind ='bar', ax = ax3, width=1)
    ax3.set_xticklabels(incidence.index.strftime('%b %d'))
    for index, label in enumerate(ax3.xaxis.get_ticklabels()):
        if index % 7 != 0:
            label.set_visible(False)
    for index, label in enumerate(ax3.xaxis.get_major_ticks()):
        if index % 7 != 0:
            label.set_visible(False)
    
    
    
    
    (incidence['rolling_incidence']*100000/population).plot(ax = ax4, lw = 4)
    ax4.axhline(y = 5,  linewidth=2, color='r', ls = '--', label="Threshold for Phase 2:\nInitial re-opening")
    ax4.axhline(y = 1,  linewidth=2, color='b', ls = '--', label="Threshold for Phase 3:\nEconomic recovery")
    ax4.legend(fontsize = 10)
    if (incidence['rolling_incidence']*100000/population).max()< 5.5:
        ax4.set_ylim(0,5.5)
    
    #print(metric)
    
    #incidence['rolling_incidence']
    #ax3.grid(which='both', alpha=1)
    ax1.set_title('(C) Cumulative cases and deaths')
    ax2.set_title('(D) Daily new tests*')
    ax3.set_title('(B) Daily incidence (new cases)')
    ax4.set_title('(A) Weekly rolling mean of incidence per 100k')
    ax3.set_ylabel('Number of individuals')
    ax4.set_ylabel('per 100 thousand')
    with _lock:
        fig.suptitle('Current situation of COVID-19 cases in California ('+ str(today)+')')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        
def plot_county(county):
    import numpy as np
    FIPSs = confirmed.groupby(['Province_State', 'Admin2']).FIPS.unique().apply(pd.Series).reset_index()
    FIPSs.columns = ['State', 'County', 'FIPS']
    FIPSs['FIPS'].fillna(0, inplace = True)
    FIPSs['FIPS'] = FIPSs.FIPS.astype(int).astype(str).str.zfill(5)
    @st.cache(ttl=3*60*60, suppress_st_warning=True)
    def get_testing_data(County):
        apiKey = 'e7c0018658814e29b12b1286bfd83ae9'
        print(type(County))
        print(County)
        if len(County) == 1:
            #print(len(County))
            f = FIPSs[FIPSs.County == County[0]].FIPS.values[0]
            #print(f)
            path1 = 'https://data.covidactnow.org/latest/us/counties/'+f+'.OBSERVED_INTERVENTION.timeseries.json?apiKey='+apiKey
            #print(path1)
            df = json.loads(requests.get(path1).text)
            #print(df.keys())
            data = pd.DataFrame.from_dict(df['actualsTimeseries'])
            data['Date'] = pd.to_datetime(data['date'])
            data = data.set_index('Date')
            #print(data.tail())
            try:
                data['new_negative_tests'] = data['cumulativeNegativeTests'].diff()
                data.loc[(data['new_negative_tests'] < 0)] = np.nan
            except: 
                data['new_negative_tests'] = np.nan
                st.text('Negative test data not avilable')
            data['new_negative_tests_rolling'] = data['new_negative_tests'].fillna(0).rolling(14).mean()
            
            
            try:
                data['new_positive_tests'] = data['cumulativePositiveTests'].diff()
                data.loc[(data['new_positive_tests'] < 0)] = np.nan
            except: 
                data['new_positive_tests'] = np.nan
                st.text('test data not avilable')
            data['new_positive_tests_rolling'] = data['new_positive_tests'].fillna(0).rolling(14).mean()
            data['new_tests'] = data['new_negative_tests']+data['new_positive_tests']
            data['new_tests_rolling'] = data['new_tests'].fillna(0).rolling(14).mean()
            data['testing_positivity_rolling'] = (data['new_positive_tests_rolling'] / data['new_tests_rolling'])*100
            #data['testing_positivity_rolling'].tail(14).plot()
            #plt.show()
            return data['new_tests_rolling'], data['testing_positivity_rolling'].iloc[-1:].values[0]
        elif (len(County) > 1) & (len(County) < 5):
            new_positive_tests = []
            new_negative_tests = []
            new_tests = []
            for c in County:
                f = FIPSs[FIPSs.County == c].FIPS.values[0]
                path1 = 'https://data.covidactnow.org/latest/us/counties/'+f+'.OBSERVED_INTERVENTION.timeseries.json?apiKey='+apiKey
                df = json.loads(requests.get(path1).text)
                data = pd.DataFrame.from_dict(df['actualsTimeseries'])
                data['Date'] = pd.to_datetime(data['date'])
                data = data.set_index('Date')
                try:
                    data['new_negative_tests'] = data['cumulativeNegativeTests'].diff()
                    data.loc[(data['new_negative_tests'] < 0)] = np.nan
                except: 
                    data['new_negative_tests'] = np.nan
                    #print('Negative test data not avilable')
                    
                try:
                    data['new_positive_tests'] = data['cumulativePositiveTests'].diff()
                    data.loc[(data['new_positive_tests'] < 0)] = np.nan
                except: 
                    data['new_positive_tests'] = np.nan
                    #print('Negative test data not avilable')
                data['new_tests'] = data['new_negative_tests']+data['new_positive_tests']
                
                new_positive_tests.append(data['new_positive_tests'])
                #new_negative_tests.append(data['new_tests'])
                new_tests.append(data['new_tests'])

            new_positive_tests_rolling = pd.concat(new_positive_tests, axis = 1).sum(axis = 1)
            new_positive_tests_rolling = new_positive_tests_rolling.fillna(0).rolling(14).mean()
        
            new_tests_rolling = pd.concat(new_tests, axis = 1).sum(axis = 1)
            new_tests_rolling = new_tests_rolling.fillna(0).rolling(14).mean()
            
            data_to_show = (new_positive_tests_rolling / new_tests_rolling)*100
            return new_tests_rolling, data_to_show.iloc[-1:].values[0]
        # else:
        #     st.text('Getting testing data for California State')
        #     path1 = 'https://data.covidactnow.org/latest/us/states/CA.OBSERVED_INTERVENTION.timeseries.json?apiKey='+apiKey
        #     df = json.loads(requests.get(path1).text)
        #     data = pd.DataFrame.from_dict(df['actualsTimeseries'])
        #     data['Date'] = pd.to_datetime(data['date'])
        #     data = data.set_index('Date')
            
        #     try:
        #         data['new_negative_tests'] = data['cumulativeNegativeTests'].diff()
        #         data.loc[(data['new_negative_tests'] < 0)] = np.nan
        #     except: 
        #         data['new_negative_tests'] = np.nan
        #         print('Negative test data not avilable')
        #     data['new_negative_tests_rolling'] = data['new_negative_tests'].fillna(0).rolling(14).mean()
            
            
        #     try:
        #         data['new_positive_tests'] = data['cumulativePositiveTests'].diff()
        #         data.loc[(data['new_positive_tests'] < 0)] = np.nan
        #     except: 
        #         data['new_positive_tests'] = np.nan
        #         st.text('test data not avilable')
        #     data['new_positive_tests_rolling'] = data['new_positive_tests'].fillna(0).rolling(14).mean()
        #     data['new_tests'] = data['new_negative_tests']+data['new_positive_tests']
        #     data['new_tests_rolling'] = data['new_tests'].fillna(0).rolling(14).mean()
        #     data['testing_positivity_rolling'] = (data['new_positive_tests_rolling'] / data['new_tests_rolling'])*100
        #     return data['new_tests_rolling'], data['testing_positivity_rolling'].iloc[-1:].values[0]
            
    
    testing_df, testing_percent = get_testing_data(County=county)
    # county_confirmed = confirmed[confirmed.Admin2.isin(county)]
    county_confirmed = confirmed[confirmed.Admin2 == county[0]]
    county_confirmed_time = county_confirmed.drop(county_confirmed.iloc[:, 0:12], axis=1).T #inplace=True, axis=1
    county_confirmed_time = county_confirmed_time.sum(axis= 1)
    county_confirmed_time = county_confirmed_time.reset_index()
    county_confirmed_time.columns = ['date', 'cases']
    county_confirmed_time['Datetime'] = pd.to_datetime(county_confirmed_time['date'])
    county_confirmed_time = county_confirmed_time.set_index('Datetime')
    del county_confirmed_time['date']
    #print(county_confirmed_time.head())
    incidence= pd.DataFrame(county_confirmed_time.cases.diff())
    incidence.columns = ['incidence']
    
    
    #temp_df_time = temp_df.drop(['date'], axis=0).T #inplace=True, axis=1
    county_deaths = deaths[deaths.Admin2==county[0]]
    population = county_deaths.Population.values.sum()
    
    del county_deaths['Population']
    county_deaths_time = county_deaths.drop(county_deaths.iloc[:, 0:11], axis=1).T #inplace=True, axis=1
    county_deaths_time = county_deaths_time.sum(axis= 1)
    
    county_deaths_time = county_deaths_time.reset_index()
    county_deaths_time.columns = ['date', 'deaths']
    county_deaths_time['Datetime'] = pd.to_datetime(county_deaths_time['date'])
    county_deaths_time = county_deaths_time.set_index('Datetime')
    del county_deaths_time['date']
    
    cases_per100k  = ((county_confirmed_time)*100000/population)
    cases_per100k.columns = ['cases per 100K']
    cases_per100k['rolling average'] = cases_per100k['cases per 100K'].rolling(7).mean()
    
    deaths_per100k  = ((county_deaths_time)*100000/population)
    deaths_per100k.columns = ['deaths per 100K']
    deaths_per100k['rolling average'] = deaths_per100k['deaths per 100K'].rolling(7).mean()
    
    
    incidence['rolling_incidence'] = incidence.incidence.rolling(7).mean()
    metric = (incidence['rolling_incidence']*100000/population).iloc[[-1]]
    st.text('Number of new cases averaged over last seven days = %s' %'{:,.1f}'.format(metric.values[0]))
    st.text("Population under consideration = %s"% '{:,.0f}'.format(population))
    st.text("Total cases = %s"% '{:,.0f}'.format(county_confirmed_time.tail(1).values[0][0]))
    st.text("Total deaths = %s"% '{:,.0f}'.format(county_deaths_time.tail(1).values[0][0]))
    st.text("% test positivity (14 day average)*= "+"%.2f" % testing_percent)
    #print(county_deaths_time.tail(1).values[0])
    #print(cases_per100k.head())
    fig = Figure(figsize=(12,8))
    #fig, ((ax4, ax3),(ax1, ax2)) = plt.subplots(2,2, figsize=(6,4))
    ((ax4, ax3),(ax1, ax2)) = fig.subplots(2,2)
    
    county_confirmed_time.plot(ax = ax1,  lw=4, color = '#377eb8')
    county_deaths_time.plot(ax = ax1,  lw=4, color = '#e41a1c')
    ax1.set_xlabel('Time') 
    ax1.set_ylabel('Number of individuals')
    
    
    
    testing_df.plot(ax = ax2,  lw=4, color = '#377eb8')
    #cases_per100k['cases per 100K'].plot(ax = ax2,  lw=4, linestyle='--', color = '#377eb8')
    #cases_per100k['rolling average'].plot(ax = ax2, lw=4, color = '#377eb8')
    
    #deaths_per100k['deaths per 100K'].plot(ax = ax2,  lw=4, linestyle='--', color = '#e41a1c')
    #deaths_per100k['rolling average'].plot(ax = ax2, lw=4, color = '#e41a1c')
    
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Number of new tests')
    
    incidence.incidence.plot(kind ='bar', ax = ax3, width=1)
    ax3.set_xticklabels(incidence.index.strftime('%b %d'))
    for index, label in enumerate(ax3.xaxis.get_ticklabels()):
        if index % 7 != 0:
            label.set_visible(False)
    for index, label in enumerate(ax3.xaxis.get_major_ticks()):
        if index % 7 != 0:
            label.set_visible(False)
    
    
    
    
    (incidence['rolling_incidence']*100000/population).plot(ax = ax4, lw = 4)
    ax4.axhline(y = 5,  linewidth=2, color='r', ls = '--', label="Threshold for Phase 2:\nInitial re-opening")
    ax4.axhline(y = 1,  linewidth=2, color='b', ls = '--', label="Threshold for Phase 3:\nEconomic recovery")
    ax4.legend(fontsize = 10)
    if (incidence['rolling_incidence']*100000/population).max()< 5.5:
        ax4.set_ylim(0,5.5)
    
    #print(metric)
    
    #incidence['rolling_incidence']
    #ax3.grid(which='both', alpha=1)
    ax1.set_title('(C) Cumulative cases and deaths')
    ax2.set_title('(D) Daily new tests')
    ax3.set_title('(B) Daily incidence (new cases)')
    ax4.set_title('(A) Weekly rolling mean of incidence per 100k')
    ax3.set_ylabel('Number of individuals')
    ax4.set_ylabel('per 100 thousand')

    with _lock:
        if len(county)<6:
            fig.suptitle('Current situation of COVID-19 cases in '+', '.join(map(str, county))+' county ('+ str(today)+')')
        else:
            fig.suptitle('Current situation of COVID-19 cases in California ('+ str(today)+')')
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
    
    import streamlit.components.v1 as components
    if len(county)<=3:
        for C in county:
            st.text(C)
            f = FIPSs[FIPSs.County == C].FIPS.values[0]
            components.iframe("https://covidactnow.org/embed/us/county/"+f, width=350, height=365, scrolling=False)
            
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

question = st.text_input("Put your query", value="What are the new case in La Crosse WI",max_chars=100)
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
        response = requests.get('http://34.66.211.120:1145/question/'+question, headers=headers)
        
        # Parse the JSON response from the server and store the result.
        result = response.json()
        county=result['County name']
        county=county.title()
        print(county)
        state=result['State name']
        print(county)
        print(state)
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
                                C=[county]
                                print(type(C))
                                plot_county(C)
                                # st.write('Well, this part is no longer available')
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
                                plot_state(state)
                                #st.write('Well, this part is no longer available')
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

                        
                          
            