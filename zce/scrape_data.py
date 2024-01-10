#%%
from bs4 import BeautifulSoup as bs
import undetected_chromedriver as uc
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import os
import pathlib
import pandas as pd
import datetime as dt

#%%
# Check if file exists, if yes then delete (to avoid duplicate files)
pathlib.Path(f'./EnglishFutureDataDaily ({dt.date.today()}).xls').unlink(missing_ok=True)

# Note, to avoid bot detection, need to import undetected_chromedriver module. Will break if version update.

chrome_options = uc.ChromeOptions()
# Open incognito browser
chrome_options.add_argument("--incognito")

# Default download directory
prefs = {
    "download.default_directory": r"C:\Users\User\Curveseries\Curveseries Private Limited - Interns\Kwok Yong\zce"
}
chrome_options.add_experimental_option("prefs",prefs)

# Disable download bubble
chrome_options.add_argument('--disable-features=DownloadBubble,DownloadBubbleV2')

# Set up driver
driver = uc.Chrome(options=chrome_options, use_subprocess=True)
driver.get("http://english.czce.com.cn/")
driver.maximize_window()

# Wait till webpage load
WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.XPATH, "//a[text()='Market Data']")))

# Hover and click Daily Trading Data
element_to_hover_over = WebDriverWait(driver,30).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, "//a[text()='Market Data']")[2]))
ActionChains(driver).move_to_element(element_to_hover_over).perform()
driver.find_elements(By.XPATH, "//a[text()='Daily Trading Data']")[1].click()

# Load page, switch to iframe
WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@name='czcehqWin']")))

# Download Excel File
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_elements(By.XPATH, "//span[@class='excle']")[0])).click()

end_time = time() + 30
# Wait till file is downloaded (timeout after 30 seconds)
while True:
    if pathlib.Path('./EnglishFutureDataDaily.xls').exists():
        break
    if time() > end_time:
        raise TimeoutError("File cannot be downloaded or took too long")

# Rename file to add today's date
os.rename('EnglishFutureDataDaily.xls', f'EnglishFutureDataDaily ({dt.date.today()}).xls')

# Close driver
driver.quit()
# %%
