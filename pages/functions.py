import os
import pandas as pd
import streamlit as st
import numpy as np
import io
import time
import pydeck
import json
import math
from logging import exception
import traceback

'''
Maykl Yakubovsky

A file for all of the functions used in the final project to keep code clean and modular

Docs and other citations:
https://deckgl.readthedocs.io/en/latest/index.html

'''

def resetDir():
    fileName = __file__
    if type(fileName.split("\\")) == list and len(fileName.split("\\"))>1:
        fileName = fileName.split("\\")[-1]
        filePath = __file__.replace(fileName,"")
    else:
        fileName = fileName.split("/")[-1]
        filePath = __file__.replace(fileName,"")
    os.chdir(filePath)
    return os.path.abspath(filePath)

def getDataframes():
    resetDir()
    os.chdir("Airport Data")
    return {
        "airport":pd.read_csv("airports.csv"),
        "comments":pd.read_csv("airport-comments.csv"),
        "frequencies":pd.read_csv("airport-frequencies.csv"),
        "countries":pd.read_csv("countries.csv"),
        "navaids":pd.read_csv("navaids.csv"),
        "regions":pd.read_csv("regions.csv"),
        "runways" : pd.read_csv("runways.csv")
        }


data = getDataframes()
@st.cache_data
def typeConvert(typeName):
    match typeName:
        case "heliport":
            return "Heliport"
        case "small_airport":
            return "Small Airport"
        case "closed":
            return "Closed Airport"
        case "seaplane_base":
            return "Seaplane Base"
        case "balloonport":
            return "Balloonport"
        case "medium_airport":
            return "Medium Airport"
        case "large_airport":
            return "Large Airport"
        case "_":
            return None
@st.cache_data
def colorSet(Type):
    match Type:
        case "Heliport":
            return [247,220,109,0.8*255]
        case "Small Airport":
            return [54,207,82,0.8*255]
        case "Closed Airport":
            return [255,0,0,0.3*255]
        case "Seaplane Base":
            return [12,123,179,0.8*255]
        case "Balloonport":
            return [137,29,191,0.8*255]
        case "Medium Airport":
            return [140,3,101,0.8*255]
        case "Large Airport":
            return [0,0,150,0.8*255]
        case "_":
            return None
@st.cache_data
def sizeSet(Type):
    match Type:
        case "Heliport":
            return 7
        case "Small Airport":
            return 10
        case "Closed Airport":
            return 5
        case "Seaplane Base":
            return 7
        case "Balloonport":
            return 7
        case "Medium Airport":
            return 12
        case "Large Airport":
            return 15
        case "_":
            return 0
@st.cache_data
def colorSetNAVAID(Type):
    match Type:
        case 'NDB':
            return [221, 252, 179,0.3*255]
        case 'DME':
            return [179, 252, 250,0.3*255]
        case 'NDB-DME':
            return [179, 252, 192,0.3*255]
        case 'VOR-DME':
            return [179, 179, 252,0.3*255]
        case 'TACAN':
            return [252, 179, 216,0.3*255]
        case 'VORTAC':
            return [252, 179, 179,0.3*255]
        case 'VOR':
            return [230, 179, 252,0.3*255]
        case "_":
            return None


'''
resetDir()
miniAirportData = pd.DataFrame(data["airport"][["ident",'name',"type","longitude_deg","latitude_deg"]])
miniAirportData["coordinates"] = miniAirportData.apply(lambda row : [row["latitude_deg"],row["longitude_deg"]],axis=1)
miniAirportData.drop("longitude_deg",axis=1,inplace=True)
miniAirportData.drop("latitude_deg",axis=1,inplace=True)
miniAirportData["type"] = miniAirportData.apply(lambda row : typeConvert(row["type"]),axis=1)
miniAirportData["color"] = miniAirportData.apply(lambda row : colorSet(row["type"]),axis=1)
miniAirportData["size"] = miniAirportData.apply(lambda row : sizeSet(row["type"]),axis=1)

miniNavAidData = pd.DataFrame(data["navaids"][["ident","name","type","longitude_deg","latitude_deg"]])
miniNavAidData["coordinates"] = miniNavAidData.apply(lambda row : [row["latitude_deg"],row["longitude_deg"]],axis=1)
miniNavAidData.drop("longitude_deg",axis=1,inplace=True)
miniNavAidData.drop("latitude_deg",axis=1,inplace=True)
miniNavAidData["color"] = miniNavAidData.apply(lambda row : colorSetNAVAID(row["type"]),axis=1)
miniNavAidData["size"] = miniNavAidData.apply(lambda row : 1,axis=1)
os.chdir("Created Data")
miniAirportData = pd.concat([miniAirportData,miniNavAidData]).reset_index()
with open("mapData.json","w") as f:
    json.dump(miniAirportData.to_json(),f)
resetDir()
'''

def getCountriesList():
    # [PY5] A dictionary where you write code to access its keys, values, or items 
    # [DA4] Filter data by one condition 
    return list(data["airport"]["iso_country"].unique())

def regionCodeToName(region):
    # [PY5] A dictionary where you write code to access its keys, values, or items 
    regions = data["regions"]
    return regions.loc[regions["code"] == region]["name"].to_string(index=False)

# [PY5]
def regionNameToCode(regionName, CN):
    regions = data["regions"]
    return regions.loc[regions["iso_country"] == CN].loc[regions["name"] == regionName]["code"].to_string(index=False)

# [PY5]
def countryCodeToName(CCode):
    return data["countries"].loc[data["countries"]["code"] == CCode]["name"].to_string(index=False)

# [PY5]
def countryNameToCode(Name):
    return data["countries"].loc[data["countries"]["name"] == Name]["code"].to_string(index=False)

# [PY5]
def getRegionsList(Country):
    # [DA4] Filter data by one condition 
    return list(data["airport"].loc[data["airport"]["iso_country"]==Country]["iso_region"].unique())

# [PY5]
def getAirportList(Region):
    # [DA4] Filter data by one condition 
    return list(data["airport"].loc[data["airport"]["iso_region"]==Region]["ident"])

# [PY5]
def getAirportNameList(Region):
    # [DA4] Filter data by one condition 
    return list(data["airport"].loc[data["airport"]["iso_region"]==Region]["name"])

# [PY5]
def nameFromICAO(ICAO):
    airports = data["airport"]
    return airports.loc[airports['ident'] == ICAO]["name"].to_string(index=False)

# [PY5]
def ICAOfromName(Name):
    airports = data["airport"]
    return airports.loc[airports['name'] == Name]["ident"].to_string(index=False)

def refreshData(sizeFactor = 5):
    with st.status("Updating Files...", expanded=True) as status:
        OverallStartTime = time.time()
        global data
        st.write("Getting Fresh Files...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.os_manager import ChromeType
        from webdriver_manager.firefox import GeckoDriverManager
        from selenium.webdriver.common.by import By  # For locating elements
        try:
            print("Updating Files")
            resetDir()
            os.chdir("Airport Data")
            options = Options()
            options.add_argument("--disable-gpu")
            options.add_argument("--headless")

            driver = webdriver.Chrome(
                service=Service(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                ),
                options=options,
            )

            siteWithLinks = "https://ourairports.com/data/"

            driver.get(siteWithLinks)

            time.sleep(1)
            #airports.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[1]/a").click()
            #airport-frequencies.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[2]/a").click()
            #airport-comments.csv 
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[3]/a").click()
            #runways.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[4]/a").click()
            #navaids.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[5]/a").click()
            #countries.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[6]/a").click()
            #regions.csv
            driver.find_element(By.XPATH,"/html/body/main/section[1]/section[2]/dl/dt[7]/a").click()
            time.sleep(5)
            driver.quit()
            os.chdir("Downloads")
            direcConts = list(os.listdir())
            if '.DS_Store' in direcConts:
                direcConts.remove(".DS_Store")
            else:
                pass

            os.chdir("..")

            for i in direcConts:
                fileName = i.strip()
                newFile = i.replace("(1)","")
                newFile = newFile.strip()
                os.replace(f"Downloads/{fileName}", f"{newFile}")
                try:
                    os.remove("Downloads/{fileName}")
                except:
                    pass
            st.toast("Files Updated!",icon='🛫')
            print("Files Updated")
        except Exception as e:
            print(traceback.format_exc())
            driver.quit()
            resetDir()
        data = getDataframes()
        resetDir()
        st.write("Recreating Map Files...")
        st.write("Building Airport Map Data")
        miniAirportData = pd.DataFrame(data["airport"][["ident",'name',"type","longitude_deg","latitude_deg"]])
        # [DA1]
        miniAirportData["coordinates"] = miniAirportData.apply(lambda row : [row["longitude_deg"],row["latitude_deg"]],axis=1)
        miniAirportData.drop("longitude_deg",axis=1,inplace=True)
        miniAirportData.drop("latitude_deg",axis=1,inplace=True)
        st.write("Constructed lat/long data")
        # [DA1]
        miniAirportData["type"] = miniAirportData.apply(lambda row : typeConvert(row["type"]),axis=1)
        st.write("Constructed Airport type data")
        # [DA1]
        miniAirportData["color"] = miniAirportData.apply(lambda row : colorSet(row["type"]),axis=1)
        st.write("Constructed Airport color data")
        # [DA1]
        miniAirportData["size"] = miniAirportData.apply(lambda row : sizeFactor * sizeSet(row["type"]),axis=1)
        st.write("Constructed Airport size data")
        st.write("Built Airport map data")

        st.write("Building Navaid Map Data")
        miniNavAidData = pd.DataFrame(data["navaids"][["ident","name","type","longitude_deg","latitude_deg"]])
        miniNavAidData["coordinates"] = miniNavAidData.apply(lambda row : [row["longitude_deg"],row["latitude_deg"]],axis=1)
        miniNavAidData.drop("longitude_deg",axis=1,inplace=True)
        miniNavAidData.drop("latitude_deg",axis=1,inplace=True)
        st.write("Constructed Navaid lat/long data")
        miniNavAidData["color"] = miniNavAidData.apply(lambda row : colorSetNAVAID(row["type"]),axis=1)
        st.write("Constructed color data")
        miniNavAidData["size"] = miniNavAidData.apply(lambda row : sizeFactor * 5,axis=1)
        st.write("Constructed Navaid size data")
        st.write("Built navaid map data")
        os.chdir("Created Data")
        miniAirportData = pd.concat([miniAirportData,miniNavAidData]).reset_index()
        with open("mapData.json","w") as f:
            json.dump(miniAirportData.to_json(),f)
        resetDir()
        st.write("Saved map data")
        OverallEndTime = time.time()
        status.update(
            label=f"Update completed in {round((OverallEndTime - OverallStartTime)/60,2)} minutes!", state="complete", expanded=False
        )


def getMunicip(AirportCode):
    muni = data["airport"].loc[data["airport"]["ident"] == AirportCode]["municipality"].to_string(index=False)
    if muni != "NaN":
        pass
    else:
        muni = "Municipality Unavailable"
    return muni

#[PY2]
#[DA3] Find Top largest or smallest values of a column
def getHighestAirport():
    highestAiport = data["airport"].loc[data["airport"]["elevation_ft"] == data["airport"]["elevation_ft"].max()]
    return highestAiport["ident"].to_string(index=False),highestAiport["elevation_ft"].to_string(index=False),highestAiport["iso_country"].to_string(index=False),highestAiport["iso_region"].to_string(index=False)

def getComments(AirportCode):
    comments = data["comments"].loc[data["comments"][' "airportIdent"'] == AirportCode]
    return comments

def getWeather(ICAO):
    os.environ['GH_TOKEN'] = st.secrets['GH_TOKEN']
    weatherSite = f"https://aviationweather.gov/data/metar/?id={ICAO}&hours=0"
    from logging import exception
    import traceback
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.common.by import By  # For locating elements
    try:
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )
        driver.get(weatherSite)
        METAR = driver.find_element(By.XPATH,"/html/body/main/div/div[4]/div[1]").text
        driver.quit()
        return METAR
    except:
        print(traceback.print_exc())
        driver.quit()
        return f"No Data found for {ICAO}"

def getAirportSuperdetail():
    superDetail = data["airport"][["ident","type","latitude_deg","longitude_deg","elevation_ft","iso_country","iso_region","municipality","iata_code","home_link","wikipedia_link"]]
    superDetail = superDetail.set_index("ident")
    freqSlice = pd.DataFrame(data["frequencies"][["airport_ident","type","description","frequency_mhz"]])
    freqSlice.rename(columns={'airport_ident': 'ident'}, inplace=True)
    freqSlice = freqSlice.set_index("ident")
    # [DA7] [DA9]
    superDetail = superDetail.join(freqSlice,how="inner",lsuffix='_airport', rsuffix='_frequency')
    return superDetail

def getAirportRunways(ICAO):
    runwaysDF = pd.DataFrame(data["runways"].loc[data["runways"]["airport_ident"] == ICAO])
    return runwaysDF

def getMapJSON():
    resetDir()
    os.chdir("Created Data")
    with open("mapData.json","r") as f:
        data = json.load(f)
    mapJson = pd.read_json(data)
    return mapJson


