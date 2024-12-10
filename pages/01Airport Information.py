import os
import pandas as pd
import streamlit as st
import time
import pydeck as pdk
from pydeck.types import String
import math

import functions as funcs

#Maykl Yakubovsky
#A Page that provides information for a selected airport
#Docs and other citations:
#https://docs.streamlit.io/
#https://docs.streamlit.io/develop/api-reference/data/st.metric
#https://docs.streamlit.io/develop/api-reference/charts/st.map
#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart

st.set_page_config(
    page_title="Airport Information",
    page_icon="🗺️",
)

st.Page(1, title="Airport Information")

#[ST4] Customized page design features: (Side Bar)
st.sidebar.success("Navigate to other pages above")

st.title("Airport Information")

st.header("Airport Details")
#[ST3] (Functional Button)
st.button("Update Data", help="Fetches Most up to date Data", on_click=funcs.refreshData, type="secondary")

# [ST1] (Selection Radio)
selectionType = st.radio('Select By:', ['ICAO', 'Airport Name'])

# [PY4] A list comprehension
Countries = [funcs.countryCodeToName(x) for x in funcs.getCountriesList()]
Countries = sorted(Countries)
# [ST2] (Dropdown)
defaultCountry = Countries.index("United States")
Country = st.selectbox(
        'Select an Country: ', Countries,
        index=defaultCountry
    )

#[PY4] A list comprehension#
availableRegions = [funcs.regionCodeToName(x) for x in funcs.getRegionsList(funcs.countryNameToCode(Country))]
availableRegions = sorted(availableRegions)
# [ST2] (Dropdown)
if Country == "United States":
    defaultRegion = availableRegions.index("Massachusetts")
else:
    defaultRegion = 0
Region = st.selectbox(
        'Select an Region/State: ', availableRegions,
        index=defaultRegion
    )
Region = funcs.regionNameToCode(Region,funcs.countryNameToCode(Country))
AirportNames = sorted(funcs.getAirportNameList(Region))
AirportICAO = sorted(funcs.getAirportList(Region))
defaultAirport = 0
if selectionType == "ICAO":
    if Region == "US-MA":
        defaultAirport = AirportICAO.index("KFIT")
    AirportCode = st.selectbox(
        'Select an Airport: ', AirportICAO,
        index = defaultAirport
    )
    AirportName = funcs.nameFromICAO(AirportCode)
elif selectionType == "Airport Name":
    if Region == "US-MA":
        defaultAirport = AirportNames.index("Fitchburg Municipal Airport")
    AirportName = st.selectbox(
        'Select an Airport: ', AirportNames,
        index = defaultAirport
    )
    AirportCode = funcs.ICAOfromName(AirportName)
else:
    AirportCode = "KFIT"
    AirportName = funcs.nameFromICAO(AirportCode)
st.header(f"{AirportName} ({AirportCode}):")
superData = funcs.getAirportSuperdetail().reset_index()
frequencies = superData.loc[superData["ident"] == AirportCode][["type_frequency","description","frequency_mhz"]]
del superData
freqtionary = {}
for k,i in frequencies.iterrows():
    freqtionary[i.loc["type_frequency"]] = {"Desc" : i.loc["description"],
                                                                         "Freq" : i.loc["frequency_mhz"]}
st.header("Radio Information:")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Type:")
    for i in freqtionary.keys():
        st.write(str(i))
with col2:
    st.subheader("Description:")
    for i in freqtionary.keys():
        st.write(str(freqtionary[i]["Desc"]))
with col3:
    st.subheader("Frequency:")
    for i in freqtionary.keys():
        st.write(str(freqtionary[i]["Freq"]) + " mhz")

st.subheader("Airport location and Map")
st.write(f"Latitude: {funcs.data["airport"].loc[funcs.data["airport"]["ident"] == AirportCode]["latitude_deg"].to_string(index=False)}, Longitude: {funcs.data["airport"].loc[funcs.data["airport"]["ident"] == AirportCode]["longitude_deg"].to_string(index=False)}" )
st.write(f"Municipality: {funcs.getMunicip(AirportCode)}")

st.write("Airport Map:")
# .to_string(index=False)

pointData = funcs.getMapJSON()

view_state = pdk.ViewState(latitude=float(funcs.data["airport"].loc[funcs.data["airport"]["ident"] == AirportCode]["latitude_deg"].to_string(index=False)), longitude=float(funcs.data["airport"].loc[funcs.data["airport"]["ident"] == AirportCode]["longitude_deg"].to_string(index=False)), zoom=10)

# Define a layer to display on a map
layer = pdk.Layer(
    "ScatterplotLayer",
    pointData,
    opacity=1,
    pickable=True,
    stroked=True,
    filled=True,
    radius_scale=15,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position="coordinates",
    get_radius="size",
    get_fill_color="color",
    get_line_color=[0, 0, 0],
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Name: {name}\nIdent: {ident}\nType: {type}"})
st.pydeck_chart(r,use_container_width=True)
st.header("Weather data from airport")
time.sleep(2)
with st.spinner("Getting METAR data from aviationweather.gov"):
    st.write(funcs.getWeather(AirportCode))