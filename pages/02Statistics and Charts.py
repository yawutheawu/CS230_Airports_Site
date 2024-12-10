import os
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rand
import time

import functions as funcs

#Maykl Yakubovsky
#A Page that provides statistical information and charts with some user interactivity
#Docs and other citations:
#https://docs.streamlit.io/
#https://docs.streamlit.io/develop/api-reference/layout/st.tabs
#https://docs.streamlit.io/develop/concepts/architecture/caching
#https://docs.streamlit.io/develop/api-reference/data/st.metric
#https://docs.streamlit.io/develop/api-reference/charts/st.map
#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.streamlit.io/develop/api-reference/status/st.status


data = funcs.getDataframes()

st.set_page_config(
    page_title="Airport Statistics",
    page_icon="📊",
)

st.Page(2, title="Airport Statistics")

#[ST4] Customized page design features: (Side Bar)
st.sidebar.success("Navigate to other pages above")
highestFieldTab, NumberAirfields, AirportsByCountry, AirportsByCountryTypes = st.tabs(["Airport Elevation", "Airport counts by Country", "Airport type distribution","Airport Types by Country"])

with highestFieldTab:
    st.subheader("Airport with the highest Field Elevation:")
    col1, col2, col3 = st.columns(3)
    # [PY2]
    # [DA3] Find Top largest or smallest values of a column
    highestAirportCode, airportHeight, airportCountry, airportRegion = funcs.getHighestAirport()
    with col1:
        st.write(f":green[{funcs.nameFromICAO(highestAirportCode)}] (:blue[:green-background[{highestAirportCode}]])")
    with col2:
        st.write(f"Field elevation of :green[{airportHeight}] ft")
    with col3:
        st.write(
            f"In region: :red-background[:green[{funcs.regionCodeToName(airportRegion)}]]\nCountry: :red-background[:green[{funcs.countryCodeToName(airportCountry)}]]")
with NumberAirfields:
    st.header("Airport Count by Country (Regardless of Operational Status)")
    AirportCountsByCountry = {x: len(data["airport"].loc[data["airport"]["iso_country"] == x]["ident"]) for x in
                              funcs.getCountriesList()}
    AirportCountsByCountry = pd.DataFrame({"Country": [str(i) for i in AirportCountsByCountry.keys()],
                                           "Num Airports": [int(i) for i in AirportCountsByCountry.values()]},
                                          index=None)

    SelectedCountries = st.multiselect("Select Countries to Plot",
                                       AirportCountsByCountry["Country"].apply(funcs.countryCodeToName),
                                       default=["United States", "Canada", "China", "Mexico"])
    SelectedCountries = [funcs.countryNameToCode(i) for i in SelectedCountries]

    # [DA2] Sort data in ascending or descending order, by one or more columns,
    # [DA4] Filter data by one condition
    SelectedCountries = AirportCountsByCountry[AirportCountsByCountry['Country'].isin(SelectedCountries)].sort_values(
        by=["Num Airports"], ascending=False)

    codeToName = pd.DataFrame({"Country Code": list(SelectedCountries["Country"]),
                               "Country Name": [funcs.countryCodeToName(i) for i in
                                                list(SelectedCountries["Country"])]}, index=None)
    st.dataframe(codeToName,use_container_width=True)
    # Plotting Bar Chart with airport count by country
    # [VIZ1]
    with st.spinner("Plotting Bar Chart"):
        x = SelectedCountries["Country"]
        y = SelectedCountries["Num Airports"]
        plt.style.use('Solarize_Light2')
        fig, ax = plt.subplots()
        plt.title('Airports by Country', fontsize=12)
        ax.bar(x, y, edgecolor="blue", linewidth=0.1)
        ax.set_ylabel("# of Airports", fontsize=3.5)
        ax.set_xlabel("Country", fontsize=6)
        plt.yticks(fontsize=4)
        plt.xticks(fontsize=4)
        for i in range(len(x)):
            plt.text(i, y.iloc[i] * 0.9, y.iloc[i], ha='center', fontsize=6, color="black",
                     bbox=dict(boxstyle="Round4,pad=0.05,rounding_size=0.1", fc="orange", ec="r", lw=0.5, alpha=0.3))
        # [VIZ1]
        st.pyplot(fig, use_container_width=True)
with AirportsByCountry:
    st.header("Airport Distribution pie chart")

    # [PY4] A list comprehension
    Countries = [funcs.countryCodeToName(x) for x in funcs.getCountriesList()]
    Countries = sorted(Countries)
    # [ST2] (Dropdown)
    defaultCountry = Countries.index("United States")
    Country = funcs.countryNameToCode(st.selectbox(
        'Select an Country: ', Countries,
        index=defaultCountry
    ))

    airportDistribution = {}
    total = 0
    for i in data["airport"].query(f"iso_country == '{Country}'")["type"].unique():
        #[DA5]
        airportDistribution[i] = len(data["airport"].query(f"iso_country == @Country and type == @i"))
        total += airportDistribution[i]

    labelers = [funcs.typeConvert(i) for i in airportDistribution.keys()]
    potentialColors = ['lightgreen', 'cyan', 'maroon', 'tab:orange', 'tab:olive',
                       'red', 'fuchsia', "dimgrey", "brown", "bisque", "burlywood",
                       "tan", "r", "g", "b", "c", "m", "y", "tab:purple", "tab:cyan",
                       "tab:pink", "tab:brown", "tab:green", "xkcd:turquoise",
                       "xkcd:sky blue", "xkcd:aqua", "xkcd:dark pink", "xkcd:pale green",
                       "xkcd:baby blue", "xkcd:dark teal", "xkcd:brick red"]
    potentialHatch = ['/', '\\', '|', '-', '+', 'x', 'o', '.', '--', '||', "xx", "//", '\\\\']
    exploder = []
    colorList = []
    hatcher = []
    for i in airportDistribution.keys():
        colorList.append(rand.choice(potentialColors))
        hatcher.append(rand.choice(potentialHatch))
        if (airportDistribution[i] / total) * 100 < 1.0:
            exploder.append(0.5)
        else:
            exploder.append(0)
    # Plotting Pie Chart that shows the types of airports
    # [VIZ2]
    with st.spinner("Plotting Pie Chart"):
        plt.style.use('Solarize_Light2')
        fig, ax = plt.subplots()
        plt.title(f'Airport types in {funcs.countryCodeToName(Country)}', fontsize=20, y=2.2, x=-1.1)
        ax.pie(list(airportDistribution.values()), labels=labelers,
               # hatch=hatcher,
               autopct='%1.1f%%',
               colors=colorList,
               textprops={'fontsize': 21},
               radius=4,
               explode=exploder
               )
        # [VIZ2]
        st.pyplot(fig, use_container_width=True)
with AirportsByCountryTypes:
    st.header("Airport Count by Country (Regardless of Operational Status)")
    CountrySelect = st.multiselect("Select Countries to Plot Airport Types:",
                                       AirportCountsByCountry["Country"].apply(funcs.countryCodeToName),
                                       default=["United States", "Canada", "China", "Mexico"])
    codeToName = pd.DataFrame({"Country Code": [funcs.countryNameToCode(r) for r in
                                                list(CountrySelect)],
                               "Country Name": list(CountrySelect)}, index=None)
    st.dataframe(codeToName,use_container_width=True)
    # Plotting Line Chart with airport count by country by type
    # [VIZ3]
    with st.spinner("Plotting Line Chart"):
        CountrySelect = [funcs.countryNameToCode(i) for i in CountrySelect]
        TypesOfAirport = data['airport']["type"].unique()
        airportDistributions = {}
        for i in TypesOfAirport:
            airportDistributions[funcs.typeConvert(i)] = []
        for j in TypesOfAirport:
            for i in CountrySelect:
                #[DA5]
                airportDistributions[funcs.typeConvert(j)].append(len(data["airport"].query(f"iso_country == @i and type == @j")))
        plt.style.use('Solarize_Light2')
        fig, ax = plt.subplots()
        potentialColors = ['lightgreen', 'cyan', 'maroon', 'tab:orange', 'tab:olive',
                           'red', 'fuchsia', "dimgrey", "brown", "burlywood",
                           "tan", "r", "g", "b", "c", "m", "y", "tab:purple", "tab:cyan",
                           "tab:pink", "tab:brown", "tab:green", "xkcd:turquoise",
                           "xkcd:sky blue", "xkcd:aqua", "xkcd:dark pink", "xkcd:pale green",
                           "xkcd:baby blue", "xkcd:dark teal", "xkcd:brick red"]
        potentialMarkers = ['1','2','3','4','+','x','|','_',0,1,2,3,4,5,6,7,8,9,10,11,".",'o','v','^','<','>','8','s','p','*','h','H','D','d','P','X',"$\u266B$"]
        potentialLinestyles = ['solid','dotted','dashed','dashdot',(0, (1, 10)),(0, (1, 1)),(0, (1, 1)),(5, (10, 3)),(0, (5, 10)),(0, (5, 5)),(0, (5, 1)),(0, (3, 10, 1, 10)),(0, (3, 5, 1, 5)),(0, (3, 1, 1, 1)),(0, (3, 5, 1, 5, 1, 5)),(0, (3, 10, 1, 10, 1, 10)),(0, (3, 1, 1, 1, 1, 1))]
        plt.title('Airport types by Country', fontsize=12)
        colors = {}
        lineType = {}
        markerStyle = {}
        for i in TypesOfAirport:
            colors[funcs.typeConvert(i)] = rand.choice(potentialColors)
            lineType[funcs.typeConvert(i)] = rand.choice(potentialLinestyles)
            markerStyle[funcs.typeConvert(i)] = rand.choice(potentialMarkers)
        for k in TypesOfAirport:
            x = []
            y = []
            for z,j in enumerate(CountrySelect):
                x.append(j)
                y.append(airportDistributions[funcs.typeConvert(k)][z])
                if len(CountrySelect) < 7:
                    ax.text(j, airportDistributions[funcs.typeConvert(k)][z], airportDistributions[funcs.typeConvert(k)][z], ha="center",fontsize=5)
            ax.plot(x, y, linewidth=1,label=funcs.typeConvert(k),
                                                                        color=colors[funcs.typeConvert(k)],
                                                                            marker=markerStyle[funcs.typeConvert(k)],
                                                                            linestyle=lineType[funcs.typeConvert(k)])
        ax.set_ylabel("# of Airports", fontsize=6)
        ax.set_xlabel("Country", fontsize=6)
        plt.legend(loc="upper right")
        plt.yticks(fontsize=4)
        plt.xticks(fontsize=4)
        # [VIZ3]
        st.pyplot(fig, use_container_width=True)
