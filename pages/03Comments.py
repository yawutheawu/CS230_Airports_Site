import os
import pandas as pd
import streamlit as st
import math

import functions as funcs

#Maykl Yakubovsky
#A Page that loads comments for an airport
#Docs and other citations:
#https://docs.streamlit.io/

st.set_page_config(
    page_title="Airport Comments",
    page_icon="💬",
)

st.Page(3, title="Airport Comments")

#[ST4] Customized page design features: (Side Bar)
st.sidebar.success("Navigate to other pages above")

st.title("Airport Comments")

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

commentsList = funcs.getComments(AirportCode)
if len(commentsList) > 0:
    #[DA8]
    commentsListRestruct = []
    for index, row in commentsList.iterrows():
        postingUserName = row[' "memberNickname"']
        commentDate = row[' "date"']
        commentSubject = row[' "subject"']
        commentBody = row[' "body"']
        if isinstance(postingUserName,str):
            pass
        else:
            postingUserName = "Unknown User"
        if isinstance(commentDate,str):
            pass
        else:
            commentDate = "Unknown Date"
        if isinstance(commentSubject,str):
            pass
        else:
            commentSubject = "Unknown Subject"
        if isinstance(commentBody,str):
            pass
        else:
            commentBody = "Unknown Body"
        commentsListRestruct.append({"Subject" : commentSubject, "Body" : commentBody, "Comment Date" : commentDate, "Comment Poster" : postingUserName})
    st.markdown("# Comments:")
    for i in commentsListRestruct:
        st.divider()
        st.markdown(f"""### Subject: {i["Subject"]}  \n##### Date/Time Posted: {i["Comment Date"]}  \n##### Username of Poster: {i["Comment Poster"]}  \n{i["Body"]}""")
else:
    st.write("No Comments at this Airport")