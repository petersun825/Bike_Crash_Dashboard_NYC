import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = (

"Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("NYC Crash Dashboard")
st.markdown("This application is a Streamlit dashboard")

@st.cache(persist = True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, delim_whitespace=False, parse_dates=[['CRASH DATE', 'CRASH TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace = True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace = True)
    data.rename(columns = {'crash date_crash time': 'date/time'}, inplace = True)
    return data

data=load_data(10000)

st.header("where are the most people injured in NYC?")
injured_people = st.slider("", 0, 19)
st.map(data.query("NUMBER OF PERSONS INJURED > @injured_people")[["latitude", "longitude"]].dropna(how="any"))


if st.checkbox("show raw data", False):
    st.subheader('Raw Data')
    st.write(data)
