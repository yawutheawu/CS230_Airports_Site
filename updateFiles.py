from logging import exception
import traceback
from selenium import webdriver  # For browser automation
from selenium.webdriver import FirefoxOptions as Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys  # For keyboard actions
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.support.ui import WebDriverWait  # For waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC  # For specifying conditions for waiting
import os # file verifications
from selenium.webdriver.common.action_chains import ActionChains
import time  # For adding small delays and timing
import streamlit as st

import functions as funcs

@st.experimental_singleton
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
    options.add_argument("--headless=new")
    options.add_experimental_option('prefs', {
            "download.default_directory": os.path.join(os.getcwd(),"Downloads"), #Set directory to save your downloaded files.
            "download.prompt_for_download": False, #Downloads the file without confirmation.
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True #Disable PDF opening.
            })
    driver = webdriver.Firefox(options=options)

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