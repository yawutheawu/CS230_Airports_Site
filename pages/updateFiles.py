from logging import exception
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By  # For locating elements
import os # file verifications
import time  # For adding small delays and timing
import streamlit as st

import functions as funcs

os.environ['GH_TOKEN'] = st.secrets['GH_TOKEN']

def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')


#[PY3] Error checking with try/except
try:
    _ = installff()
    print("Updating Files")
    funcs.resetDir()
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
    funcs.resetDir()