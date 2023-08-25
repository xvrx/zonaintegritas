from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import os,time, random, shutil

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from djponline.workaround import NotifyObj as Notify
from djponline.workaround.captchSc import captchaAdjust 

def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(1)
    actions.perform()

def deleteCache(driver):
    driver.get('about:preferences#general')
    driver.execute_script("document.querySelector('#category-privacy > label:nth-child(2)').click()")
    driver.execute_script("document.querySelector('#clearHistoryButton').click()")
    perform_actions(driver, Keys.TAB * 8 + Keys.ENTER)  

def waitUntil (driver,element : str, sleep : int, msg:str = None):
    if msg == None:
        print('waiting for element..')
    else:
        print(f"waiting for {msg} ...")
    # if 
    while True:
        try:
            driver.find_element(by=By.CSS_SELECTOR , value=element )
            break
        except:
            time.sleep(sleep)
            continue

def trinfo (data):
    print(f"\n 🦴 type: {type(data)} || 🔎 value: {str(data)} \n")

def cprint(stat, msg):
    if stat == -1:
        print(f"\n 🔴 {msg}  \n")
    if stat == 0:
        print(f"\n 🟡 {msg}  \n")
    if stat == 1:
        print(f"\n 🟢 {msg}  \n")

# def niggabolt ():
def promptCaptcha (driver, element, destination):
    print('captcha confirm...')
    # try:
    waitUntil(driver, element,2)
    captchaImage = driver.find_element(by=By.CSS_SELECTOR, value=f"{element}")
    print("element found!")
    location = captchaImage.location
    size = captchaImage.size
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    captchaAdjust(png, location, size)
    # prompt input captcha
    captchaInput = Notify.DisplayCaptcha("captch.png", "login-test").runAttempt()
    # retrieving capthca
    shutil.copy('captch.png',destination+"/"+f"{captchaInput}.png")
    return captchaInput
    # except Exception as err:
    #     print('some niggas shitty as hell!')
    #     return 'error unkown'


def includeText (intendedTxt:str,content:str):
    if int(content.find(intendedTxt)) > -1:
        return True
    else:
        return False

