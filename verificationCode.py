from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as waitfr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium. webdriver. common. keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time,random,os, csv
from csv import reader, writer
import djponline.workaround.NotifyObj as Notify
from workaround.captchSc import captchaAdjust


#! ERROR
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,WebDriverException
from selenium.common.exceptions import JavascriptException

# ! GECKO
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile



# profile.set_preference("pdfjs.disabled", False)

# profile.set_preference("general.useragent.override", useragent)
# options.add_argument('--headless')

# options = webdriver.ChromeOptions()
# downloaddir = f"{os.getcwd()}/downloads"
# prefs = {"download.default_directory" : f"{downloaddir}"}
from selenium.webdriver.firefox.options import Options
options = Options()

options.add_argument("--start-maximized")


options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", "./downloads")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
# prefs = {"profile.default_content_settings.popups": 0,
#             "download.default_directory": r"C:\\Users\\Rustacean\Desktop\\eform0\\", # IMPORTANT - ENDING SLASH V IMPORTANT
#             "directory_upgrade": True}
            

driver = webdriver.Firefox(executable_path="C:\\geckodriver.exe", options=options)


def obtainVerificationCode(email, nama):
    emailnesia = email[:-14]
    driver.get(f"http://mailnesia.com/mailbox/{emailnesia}")
    driver.switch_to.window(driver.window_handles[0])
    # wait until
    while True:
        try:
            time.sleep(3)
            driver.refresh()
            WebDriverWait(driver, 10).until(waitfr.presence_of_element_located((By.CLASS_NAME, "emailheader")))
        except NoSuchElementException:
            print('waiting for confirmation email!')
            continue
        except WebDriverException:
            print('(time out) waiting for aktivasi email!')
            continue
        break

    Textid = driver.find_elements_by_css_selector('.emailheader')[0].get_attribute('id')
    latestMail = driver.find_elements_by_css_selector('.emailheader td:nth-child(4)')[0]
    textTitle = latestMail.get_attribute("textContent")

    print('text Content :', textTitle)
    print('element id is', Textid)

    # test if lupa password
    a = textTitle.find('Verifikasi')

    if int(a) >= 0:
        print('obtaining kode verifikasi...')
        # click #emailbody_(id)
        driver.execute_script(f"document.getElementById({str(Textid)}).click()")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0]) # in case ads pop up
        time.sleep(1)
        # get text content of verifikasi
        y = driver.find_elements_by_tag_name('strong')
        kode = y[2].get_attribute("textContent")
        print('kode verikasi :', kode)
        
        print(f'verification for {nama} is obtained!')
        driver.delete_all_cookies()
        return kode
    else:
        print('kode verifikasi not found!')


# with open('./src/app.csv') as belumLapor:
#     readCsv = csv.DictReader(belumLapor, delimiter=',')
#     for line in readCsv:
#         print(line)


import pandas as pd


# after manually making a column for index in the first column [0]
# use index_col=[0] as a parameter in pd.read_csv
# to prevent unnamed : 0 column from being created on loc function

# wp = pd.read_csv('./src/indexed.csv', delimiter=',', index_col=[0] )
# wpdict = wp.to_dict()
# print(wp)
# print(wp.columns)
# print(wp['NAMA_WP'])
# print(wp[['NAMA_WP', 'EMAIL']])
# specific column and row (r,c)
# print(wp.iloc[0,2])

# if the process is interrupted, u may skip iteration within following range
done = range(0,21)

wp = pd.read_csv('./src/indexed.csv', delimiter=',', index_col=[0] )
## scrape 'kode verifikasi' for each email and write it in app3.csv
for index, row in wp.iterrows():
    if index in done:
        continue
    bruh = obtainVerificationCode(row['EMAIL'], row['NAMA_WP'])
    print('bruh is :', bruh)
    if len(bruh) > 1:
        wp.loc[index,'aktivasi'] = bruh
        wp.to_csv('./src/app3 (continue).csv', index=False)
    time.sleep(1)




    