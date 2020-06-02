import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

DATA_URL = (
#"\Users\peter\OneDrive\Desktop\Work\
"Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("NYC Dashboard")
st.markdown("This application is a Streamlit dashboard")

@st.cache(persist = True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH DATE', 'CRASH TIME']])
    data = data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace = False)
    lowercase = lambda x: str(x).lower().replace(' ','_')
    data.rename(lowercase, axis = 'columns', inplace = True)
    data.rename(columns = {'crash_date_crash_time': 'date/time'}, inplace = True)
    return data

data=load_data(10000)

st.header("where are most of the people injured in NYC based?")
injured_people = st.slider("", 0, 19)
st.map(data.query("number_of_persons_injured >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("how many collisions occur during a given time of day?")

hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions between %i:00 & %i:00" %(hour, (hour+1)))
midpoint_lat = np.average(data['latitude'])
midpoint_long = np.average(data['longitude'])

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude": midpoint_lat,
        "longitude": midpoint_long,
        "zoom":12,
        "pitch":50,
    },

    layers = [
        pdk.Layer(
        "hexagonLayer",
        data = data[['date/time', 'latitude', 'longitude']],
        get_position= ['latitude', 'longitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0,1000],
        ),
    ],

))

if st.checkbox("show raw data", False):
    st.subheader('Raw Data')
    st.write(data)
