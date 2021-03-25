import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image
pd.set_option("display.max_columns", 100)

st.set_page_config(
    page_title="COVID-19",
    layout="wide",
    initial_sidebar_state="expanded",
)

df = pd.read_csv('coronanet.csv')

confirmed_cases_full = df.groupby('country')['confirmed_cases'].max().sort_values(ascending=False).to_frame().reset_index()
deaths_full = df.groupby('country')['deaths'].max().sort_values(ascending=False).to_frame().reset_index()
recovered_full = df.groupby('country')['recovered'].max().sort_values(ascending=False).to_frame().reset_index()

percentages = pd.merge(confirmed_cases_full, deaths_full, how='left').merge(recovered_full, how='left')

percentages['%_deaths'] = (percentages['deaths']/percentages['confirmed_cases'])*100
percentages['%_recovered'] = (percentages['recovered']/percentages['confirmed_cases'])*100

pages = st.sidebar.radio('Page Navigation', ['Overview', 'Exploring USA'])

if pages == 'Overview':
    option = st.selectbox(
        'Choose the statistic to review:',
        ('Confirmed Cases', 'Deaths', '% Deaths', 'Recovered', '% Recovered'))
    number = int(st.text_input('Choose the number of countries to be included. Input a number not more than 201:', '20'))
    
    if st.button('Show Plot'):
        if option == 'Confirmed Cases':
            new_df = percentages[['country', 'confirmed_cases']].sort_values(by='confirmed_cases', ascending=False).head(number)
            fig = px.bar(new_df, x='country', y='confirmed_cases',
                 labels={'country':'Country', 'confirmed_cases':'Confirmed Cases'},
                 title='COVID-19 CONFIRMED CASES', color_discrete_sequence=['#F6F926'],
                 height=600)
            st.plotly_chart(fig)

        elif option == 'Deaths':
            new_df = percentages[['country', 'deaths']].sort_values(by='deaths', ascending=False).head(number)
            fig = px.bar(new_df, x='country', y='deaths',
                         labels={'country':'Country', 'deaths':'Deaths'},
                         title='COVID-19 DEATHS', color_discrete_sequence=['#D62728'],
                         height=600)
            st.plotly_chart(fig)

        elif option == '% Deaths':
            new_df = percentages[['country', '%_deaths']].sort_values(by='%_deaths', ascending=False).head(number)
            fig = px.bar(new_df, x='country', y='%_deaths',
                         labels={'country':'Country', '%_deaths':'% Deaths'},
                         title='% COVID-19 DEATHS', color_discrete_sequence=['#D62728'],
                         height=600)
            st.plotly_chart(fig)

        elif option == 'Recovered':
            new_df = percentages[['country', 'recovered']].sort_values(by='recovered', ascending=False).head(number)
            fig = px.bar(new_df, x='country', y='recovered',
                         labels={'country':'Country', 'recovered':'Recovered'},
                         title='COVID-19 RECOVERIES', color_discrete_sequence=['#1F77B4'],
                         height=600)
            st.plotly_chart(fig)

        elif option == '% Recovered':
            new_df = percentages[['country', '%_recovered']].sort_values(by='%_recovered', ascending=False).head(number)
            fig = px.bar(new_df, x='country', y='%_recovered',
                         labels={'country':'Country', '%_recovered':'% Recovered'},
                         title='% COVID-19 RECOVERIES', color_discrete_sequence=['#1F77B4'],
                         height=600)
            st.plotly_chart(fig)

if pages == 'Exploring USA':
    
    col1, col2 = st.beta_columns(2)
    
    col1.image('first.png', width=500)
    col2.image('second.png', width=500)
    
    usa = df[df['country'] == 'United States of America']
    usa_prov = tuple(sorted(usa['province'].dropna('').unique()))
    
    usa_df = usa.groupby(['province', 'date_announced'])['type'].value_counts().to_frame()\
            .rename(columns={'type':'Type'}).drop(columns=['Type'], axis=1).reset_index()
    usa_df['date_announced'] = pd.to_datetime(usa_df['date_announced'])
    actions = usa.groupby(['province', 'date_announced'])['type'].value_counts().to_frame().drop(columns=['type'], axis=1).reset_index()
    actions['date_announced'] = pd.to_datetime(actions['date_announced'], infer_datetime_format=True)
   
    option2 = str(st.selectbox('Pick a state!', usa_prov))
    if st.button('Show timeline of COVID-19 protocols'):
        actions_new = actions[actions['province'] == option2].sort_values(by='date_announced')
        actions_new['date_announced'] = actions_new['date_announced'].astype(str)
        st.write(actions_new)