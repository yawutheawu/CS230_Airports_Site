import os
import pandas as pd
import streamlit as st

import functions as funcs

#Maykl Yakubovsky
#A Page that provides statistical information and charts with some user interactivity
#Docs and other citations:
#https://docs.streamlit.io/
#https://docs.streamlit.io/develop/api-reference/data/st.metric
#https://docs.streamlit.io/develop/api-reference/charts/st.map
#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart

data = funcs.getDataframes()

st.set_page_config(
    page_title="Data",
    page_icon="📊",
)

st.Page(4, title="Data Tabels")

#[ST4] Customized page design features: (Side Bar)
st.sidebar.success("Navigate to other pages above")

st.header("Dataframes:")
for i in data.keys():
    st.write(f"{i} data:")
    st.dataframe(data[i])