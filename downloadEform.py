from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as waitfr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium. webdriver. common. keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time,random,os
import djponline.workaround.NotifyObj as Notify
from workaround.captchSc import captchaAdjust


#! ERROR
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import JavascriptException

# ! GECKO
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile




# options = webdriver.FirefoxOptions()
# profile.set_preference("pdfjs.disabled", False)

# profile.set_preference("general.useragent.override", useragent)
# options.add_argument('--headless')

options = webdriver.ChromeOptions()
downloaddir = f"{os.getcwd()}/downloads"
# prefs = {"download.default_directory" : f"{downloaddir}"}

options.add_argument("--start-maximized")
# prefs = {"profile.default_content_settings.popups": 0,
#             "download.default_directory": r"C:\\Users\\Rustacean\Desktop\\eform0\\", # IMPORTANT - ENDING SLASH V IMPORTANT
#             "directory_upgrade": True}
            
# options.add_experimental_option("prefs", prefs)

# chromeOptions.add_experimental_option("prefs",prefs)

# desired_caps = {'prefs': {'download': {'default_directory': '/Users/thiagomarzagao/Desktop/downloaded_files/'}}}
# options.set_preference("browser.download.panel.shown", False)
# options.set_preference("browser.download.useDownloadDir", True)

# ##not to use default Downloads directory
# options.set_preference("browser.download.folderList", 2)

# options.set_preference("browser.download.manager.showWhenStarting", False)

# options.set_preference("browser.download.dir", downloaddir)
# # # profile.set_preference("browser.download.dir", downloaddir)
# options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
# options.set_preference("browser.helperApps.neverAsk.openFile","application/pdf")


driver = webdriver.Chrome(executable_path = "C:\\chromedriver.exe", options= options)
driver.get("https://djponline.pajak.go.id/account/login")
# driver = webdriver.Firefox(executable_path="C:\\geckodriver.exe", options=options, firefox_profile=profile)

# login
def downloadPDF(npwp,nama, passw0="pajak123"):
    while True:
        try:
            WebDriverWait(driver, 5).until(waitfr.presence_of_element_located((By.CLASS_NAME, "swal2-close"))) 
            driver.find_element_by_class_name("swal2-close").click()
            time.sleep(1)
            ##  LOGIN TEST
            driver.execute_script(f"document.getElementById('username').value='{npwp}'")
            passw = driver.find_element(by=By.ID, value="password")
            passw.send_keys(passw0)
            # captcha get image
            captchaImage = driver.find_element_by_css_selector("#captchaImage")
            location = captchaImage.location
            size = captchaImage.size
            png = driver.get_screenshot_as_png()  # saves screenshot of entire page
            captchaAdjust(png, location, size)
            # prompt input captcha
            captchaLogin = Notify.DisplayCaptcha("captch.png", "login-test").runAttempt()
            catpchaInput = driver.find_element_by_css_selector("#captchaTxt")
            catpchaInput.send_keys(captchaLogin)
            time.sleep(1)
            driver.find_element(by=By.ID, value="btnSubmit").click()
            WebDriverWait(driver, 10).until(waitfr.presence_of_element_located((By.CLASS_NAME, "kt-menu__link-text")))
            # driver.execute_script('window.open('');')
            # driver.switch_to.window(driver.window_handles[1])
            driver.get("https://eform-web.pajak.go.id/efile/spt")
            time.sleep(1)
            driver.get("https://eform-web.pajak.go.id/efile/spt")
            driver.execute_script("document.getElementById('rbs11').click()")
            driver.execute_script("document.querySelector('#divP > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)').click()")

            WebDriverWait(driver, 5).until(waitfr.presence_of_element_located((By.ID, "thnPajak")))
            driver.execute_script("document.getElementById('thnPajak').selectedIndex = 1; document.getElementById('thnPajak').dispatchEvent(new Event('change'));")
        except JavascriptException:
            time.sleep(1)
            continue
        break
    
    while True:
        try:
            time.sleep(2)
            # downloadEfform = driver.find_element_by_id('btnSubmit')
            # ActionChains(driver).key_down(Keys.ALT).execute_script("document.getElementById('btnSubmit').click()").key_up(Keys.ALT).perform()
            driver.execute_script("document.getElementById('btnSubmit').click()")
        except ElementClickInterceptedException:
            time.sleep(1)
            continue
        break
    print(f'{nama} - eform downloaded!')
    time.sleep(5)

    while True:
        try:
            time.sleep(2)
            # downloadEfform = driver.find_element_by_id('btnSubmit')
            # ActionChains(driver).key_down(Keys.ALT).execute_script("document.getElementById('btnSubmit').click()").key_up(Keys.ALT).perform()
            driver.execute_script("document.querySelector('.flaticon2-user.kt-font-warning').click()")
            driver.execute_script("document.querySelector('.btn.btn-label.btn-label-brand.btn-sm.btn-bold').click()")
        except ElementClickInterceptedException:
            time.sleep(1)
            continue
        except JavascriptException:
            time.sleep(1)
            continue
        break
    time.sleep(2)


# loop download
import csv

with open('./src/app.csv') as belumLapor:
    readCsv = csv.DictReader(belumLapor, delimiter=',')

    for line in readCsv:
        # print(line['NPWP'], line['EMAIL'])
        downloadPDF(line['NPWP'], line['NAMA_WP'])




