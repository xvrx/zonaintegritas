import random
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as waitfr
from selenium.webdriver.common.by import By
import time, shutil
from pprint import pprint
from workaround.captchSc import captchaAdjust
import workaround.NotifyObj as Notify

def runCaptcha (driver, element, destination):
    print('some niggas try to shoot us in the ass')
    # return 'color of your skin dont matter!'
    # #  value = #captchaImage
    try:
        # print('looking for captcha element')
        # captchaImage = driver.find_element(by=By.CSS_SELECTOR, value={element})
        # location = captchaImage.location
        # size = captchaImage.size
        # png = driver.get_screenshot_as_png()  # saves screenshot of entire page
        # captchaAdjust(png, location, size)
        # prompt input captcha
        captchaLogin = Notify.DisplayCaptcha("../captch.png", "login-test").runAttempt()
        # retrieving capthca
        shutil.copy('captch.png', f"/workaround/collection3/{captchaLogin}.png")
        return captchaLogin
    except Exception as err:
        print('error unknown! :'+ err)
        return 'error unkown'

b = runCaptcha()

import os
print(os.getcwd())