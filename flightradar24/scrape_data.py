#%%
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import pathlib
import pandas as pd
import datetime as dt

#%% All flights
# Check if file exists, if yes then delete (to avoid duplicate files)
pathlib.Path("./total-number-of-flights.csv").unlink(missing_ok=True)

chrome_options = ChromeOptions()
# Open incognito browser
chrome_options.add_argument("--incognito")

# Default download directory
prefs = {
    "download.default_directory": r"xxx\flightradar24"} # Dummy default directory
chrome_options.add_experimental_option("prefs",prefs)

# Disable download bubble
chrome_options.add_argument('disable-features=DownloadBubble,DownloadBubbleV2')

# Set up driver
driver = Chrome(chrome_options)
driver.get("https://www.flightradar24.com/data/statistics")
driver.maximize_window()

# Click "Accept Cookies"
button = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]')))
button.click()

# Click "Number of flights" and unclick "Moving Average"
## Note "2024 Number of flights" is activated by default
for i in range(2020, 2024):
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, f"//*[name() = 'g']/*[text()='{i} Number of flights']"))).click()
    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, f"//*[name() = 'g']/*[text()='{i} 7-day moving average']"))).click()

## Unclick "2024 7-day moving average"
WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, f"//*[name() = 'g']/*[text()='2024 7-day moving average']"))).click()

# Download CSV file
menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//*[name()='g' and contains(@class, 'highcharts-no-tooltip highcharts-button highcharts-contextbutton')]")))
menu.click()
download_button = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='highcharts-menu-item' and text()='Download CSV']")))
download_button.click()

sleep(5)

# Read CSV to Python
file = pd.read_csv("xxx/flightradar24/total-number-of-flights.csv") # Dummy directory

# Drop suffix
file.columns = file.columns.str.strip(" Number of flights")

# Pivot longer, drop NA values (no 29 Feb in non-leap years)
file = pd.melt(file, id_vars = ['DateT'], value_vars=['2020','2021','2022','2023','2024'], var_name = 'Year', value_name = 'Total Number of flights').dropna()

# Rename column DateT to Date
file.rename(columns={"DateT": "Date"}, inplace=True)

# Convert string to datetime
file['Date'] = pd.to_datetime(file['Date'])

# Convert date to correct year
file['Date'] = file.apply(lambda row: row.Date.replace(year=int(row.Year)), axis=1)

# Drop column Year
file.drop(labels=['Year'], axis = 1, inplace=True)

#%% Commercial flights
# Check if file exists, if yes then delete (to avoid duplicate files)
pathlib.Path("./number-of-commercial-fli.csv").unlink(missing_ok=True)

# Click "Number of flights" and unclick "Moving Average"
## Note "2024 Number of flights" is activated by default
for i in range(2020, 2024):
    WebDriverWait(driver,5).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, f"//*[name() = 'g']/*[text()='{i} Number of flights']")[1])).click()
    WebDriverWait(driver,5).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, f"//*[name() = 'g']/*[text()='{i} 7-day moving average']")[1])).click()

## Unclick "2024 7-day moving average"
WebDriverWait(driver,5).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, f"//*[name() = 'g']/*[text()='2024 7-day moving average']")[1])).click()

# Download CSV file
menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, "//*[name()='g' and contains(@class, 'highcharts-no-tooltip highcharts-button highcharts-contextbutton')]")[1]))
menu.click()
download_button = WebDriverWait(driver,5).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, "//li[@class='highcharts-menu-item' and text()='Download CSV']")[1]))
download_button.click()

sleep(5)

# Read CSV to Python
file2 = pd.read_csv("xxx/flightradar24/number-of-commercial-fli.csv") # Dummy directory

# Drop suffix
file2.columns = file2.columns.str.strip(" Number of flights")

# Pivot longer, drop NA values (no 29 Feb in non-leap years)
file2 = pd.melt(file2, id_vars = ['DateT'], value_vars=['2020','2021','2022','2023','2024'], var_name = 'Year', value_name = 'Number of commercial flights').dropna()

# Rename column DateT to Date
file2.rename(columns={"DateT": "Date"}, inplace=True)

# Convert string to datetime
file2['Date'] = pd.to_datetime(file2['Date'])

# Convert date to correct year
file2['Date'] = file2.apply(lambda row: row.Date.replace(year=int(row.Year)), axis=1)

# Drop column Year
file2.drop(labels=['Year'], axis = 1, inplace=True)

# Combine 2 dataframes
file['Number of commercial flights'] = file2['Number of commercial flights']
# file['Date'] = pd.to_datetime(file['Date']).dt.strftime('%Y-%m-%d')
file.set_index(['Date'], inplace=True)

# Export to xlsx file
pathlib.Path("./flightradar24-statistics.xlsx").unlink(missing_ok=True)
file.to_excel('flightradar24-statistics.xlsx')
# %%
