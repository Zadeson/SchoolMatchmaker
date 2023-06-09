import streamlit as st
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time

# Title/Format
st.set_page_config(layout='wide')
st.title("SchoolMatchmaker")
# load csv data

@st.cache_data
def load_data():
    columns = ['LSTATE', 'SCH_NAME', 'LSTREET1', 'LCITY', 'TOTAL', 'STUTERATIO', 'SCHOOL_TYPE_TEXT', 'SCHOOL_LEVEL', 'LATCOD', 'LONCOD', 'SY_STATUS_TEXT', 'AMALM','AMALF','ASALM','ASALF','HIALM','HIALF','BLALM','BLALF','WHALM','WHALF','HPALM','HPALF','TRALM','TRALF']
    df_schools = pd.read_csv("Data\Public_School_Characteristics_2020-21.csv", usecols=columns)
    return df_schools
@st.cache_data
def clean_and_group_data():
    df_schools = load_data()

    # Filter and clean data
    df_schools.drop_duplicates(inplace=True)
    df_schools.reset_index(drop=True, inplace=True)

    # Group data
    grouped_columns = ['LSTATE', 'SCH_NAME', 'LSTREET1', 'LCITY', 'TOTAL', 'STUTERATIO', 'SCHOOL_TYPE_TEXT', 'SCHOOL_LEVEL', 'LATCOD', 'LONCOD', 'SY_STATUS_TEXT']
    df_grouped = df_schools.groupby("SCH_NAME", as_index=False)[grouped_columns].max()

    return df_grouped

df_schools = load_data()
df_grouped = clean_and_group_data()

# Set result DataFrame
df_result = df_grouped.copy()

col1, col2 = st.columns([1, 2])
with st.sidebar:
    with st.container():
        stateoption = st.selectbox(
            'Select a State:',
            ("AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", 
             "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", 
             "WI", "WY"))
        statedata = df_schools.loc[(df_schools["LSTATE"] == stateoption)]

        cities = sorted(df_schools.loc[df_schools['LSTATE'] == stateoption, 'LCITY'].unique())
        cityoption = st.selectbox('Select a city:', cities)

        # Add a dropdown menu to select a school
        schools = sorted(df_schools.loc[df_schools['LCITY'] == cityoption, 'SCH_NAME'].unique())
        schooloption = st.selectbox('Select a school:', schools)

        # Filter the data to the selected school
        school_data = df_schools[df_schools['SCH_NAME'] == schooloption]
        

with col1:
    with st.container():
        st.subheader('Demographics')
        if not school_data.empty:
            if not school_data.empty:
                male_total = school_data[['AMALM', 'ASALM', 'HIALM', 'BLALM', 'WHALM', 'HPALM', 'TRALM']].sum().sum()
                female_total = school_data[['AMALF', 'ASALF', 'HIALF', 'BLALF', 'WHALF', 'HPALF', 'TRALF']].sum().sum()
                white_total = school_data[['WHALM', 'WHALF']].sum().sum()
                black_total = school_data[['BLALM', 'BLALF']].sum().sum()
                hispanic_total = school_data[['HIALM', 'HIALF']].sum().sum()
                asian_total = school_data[['ASALM', 'ASALF']].sum().sum()
                native_total = school_data[['AMALM', 'AMALF', 'HPALM', 'HPALF']].sum().sum()
                mixed_total = school_data[['TRALM', 'TRALF']].sum().sum()

                labels = ['White', 'Black/African American', 'Hispanic/Latino', 'Asian', 'Native', 'Mixed']
                values = [white_total, black_total, hispanic_total, asian_total, native_total, mixed_total]

                fig = go.Figure(
                    go.Pie(
                        labels=labels,
                        values=values,
                        hoverinfo='label+percent',
                        textinfo='label',
                        hole=.3
                    )
                )
                st.plotly_chart(fig)
            else:
                st.write(f"No data found for {schooloption}")
