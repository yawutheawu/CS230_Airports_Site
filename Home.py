import os
import pandas as pd
import streamlit as st

import functions as funcs


#Maykl Yakubovsky
#A file that acts as a main with a focus on streamlit functionality
#Docs and other citations:
#https://docs.streamlit.io/
#https://docs.streamlit.io/develop/concepts/multipage-apps

st.set_page_config(
    page_title="Airport Data Analysis",
    page_icon="✈️",
)

st.header("Airport Data Analysis Landing Page")
st.markdown("""Select a page from the sidebar on the __:blue-background[left]__""")
#[ST4] Customized page design features: (Side Bar)
st.sidebar.success("Select a Page above.")