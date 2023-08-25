from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as waitfr
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint
from djponline.workaround.captchSc import captchaAdjust
from djponline.workaround import waitUntil, cprint, includeText, perform_actions
# from djponline.workaround import runCaptcha
from djponline.workaround import promptCaptcha
from djponline.workaround import NotifyObj as Notify

#! ERROR
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
# driver = webdriver.Firefox(executable_path="C:\\geckodriver.exe")


# class confirmLupa (self, driver, emailID ):
#     def __init__(self):
#         self.driver = driver
#         self.emailID = emailID

def closeTabs (driver):
    # close unecessary tabs
    try:
        curr = driver.current_window_handle
        print('current tab initialized!')
        for handle in driver.window_handles:
            try:
                tabz = 0
                driver.switch_to.window(handle)
                if handle != curr:
                    driver.close()
                    tabz += 1
                print(f'{tabz} Tab closed!')
            except NoSuchWindowException:
                pass
    except NoSuchWindowException:
        pass
    print('all unecessary tabs have been closed!')


def confirmLupa(driver, npwp, efin, mailnesia):
    print('resetting ...')
    driver.get("https://djponline.pajak.go.id/account/lupapassword")
    waitUntil(driver, "#efin", 2)
    driver.execute_script("document.getElementById('cbEmail').click()")
    driver.execute_script(f"document.getElementById('npwp').value='{npwp}'")
    driver.find_element(by=By.ID, value="efin").send_keys(efin)
    time.sleep(1)
    driver.find_element(by=By.ID, value="email").send_keys(mailnesia)

    #email
    driver.execute_script(f"document.getElementById('email').value='{mailnesia}'")

    # input captcha
    promptedCaptcha = promptCaptcha(driver, "#captchaImage", "./djponline/workaround/collection3")
    driver.execute_script(f"document.getElementById('captcha').value='{promptedCaptcha}'")
    # return ''
    time.sleep(1)
    driver.find_element(by=By.ID, value="btnVerifikasi").click()
    # driver.execute_script(f"document.getElementById('btnVerifikasi').click()")
    # perform_actions(driver, Keys.ENTER)
    
    waitUntil(driver, "#swal2-content", 2)
    lupaConfirm = driver.execute_script("return document.querySelector('#swal2-content').textContent")
    
    while True:
        print('waiting if link is sent!')
        if includeText("dikirim ke email Anda", lupaConfirm):
            break
        else:
            time.sleep(2)
            continue

    print('going to mailnesia..')

    emailID = mailnesia[:-14]
    try:
        ## new window
        driver.execute_script('''window.open("","_blank");''')

        # driver.execute_script('window.open('');')
        driver.switch_to.window(driver.window_handles[1])

        driver.get(f"http://mailnesia.com/mailbox/{emailID}")

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


        # wait until
        waitUntil(driver, ".emailheader", 2)
        # Textid = driver.find_elements_by_css_selector('.emailheader')[0].get_attribute('id') 
        Textid = driver.find_elements(by=By.CSS_SELECTOR, value=".emailheader")[0].get_attribute('id')
        # latestMail = driver.find_elements_by_css_selector('.emailheader td:nth-child(4)')[0]
        latestMail = driver.find_elements(by=By.CSS_SELECTOR, value=".emailheader td:nth-child(4)")[0]
        textTitle = latestMail.get_attribute("textContent")

        print('element located!')

        print('text Content :', textTitle)
        print('element id is', Textid)

        # test if lupa password
        a = textTitle.find('Lupa Password')

        if int(a) > -1:
            # click #emailbody_(id)
            driver.execute_script(f"document.getElementById({str(Textid)}).click()")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1]) # in case ads pop up
            print('back to DJP online...')
            driver.execute_script("document.querySelector('.es-button-border>a:nth-child(1)').click()")
            time.sleep(1)
            waitUntil(driver, "#pswBaru", 2)

            driver.find_element(by=By.CSS_SELECTOR, value="#pswBaru").send_keys('123456')
            # driver.find_element_by_id("pswBaru").send_keys('123456')
            driver.find_element(by=By.CSS_SELECTOR, value="#rePswBaru").send_keys('123456')
            # driver.find_element_by_id("rePswBaru").send_keys('123456')

            captchLupaPass = promptCaptcha(driver, "#captchaImage", "./djponline/workaround/collection3")
            driver.execute_script(f"document.getElementById('captcha').value='{captchLupaPass}'")

            # driver.find_element_by_css_selector("#captcha").send_keys(captchLupaPass)
            driver.find_element(by=By.CSS_SELECTOR, value="#captcha").send_keys(captchLupaPass)
            # driver.find_element_by_css_selector("#btnVerifikasi").click()
            driver.find_element(by=By.CSS_SELECTOR, value="#btnVerifikasi").click()
            time.sleep(1)
            waitUntil(driver, ".swal2-success-ring", 2)
            lupaPasswordResult = driver.execute_script("return document.querySelector('#swal2-content').textContent")
            print(lupaPasswordResult)
            closeTabs(driver)
            return f'result : {lupaPasswordResult}'
        else:
            print('password reset mail is not found!')
            return 'email not found!'
    except Exception as err:
        print(f"error : {err}")
        return f'error {str(err)}'










def aktivasi (driver, npwp, efin, mailnesia, nohp):
    print('aktivasi akun ...')
    driver.get("https://djponline.pajak.go.id/account/registrasi")
    waitUntil(driver, "#efin", 2)

    driver.execute_script(f"document.getElementById('npwp').value='{npwp}'")
    driver.find_element(by=By.ID, value="efin").send_keys(efin)
    time.sleep(1)

    # input captcha
    promptedCaptcha = promptCaptcha(driver, "#captchaImage", "./djponline/workaround/collection3")
    driver.execute_script(f"document.getElementById('captcha').value='{promptedCaptcha}'")
    
    time.sleep(1)
    driver.find_element(by=By.ID, value="btnVerifikasi").click()
    

    waitUntil(driver, "#noTelp", 2)
    driver.execute_script(f"document.getElementById('email').value='{mailnesia}'")
    driver.execute_script(f"document.getElementById('noTelp').value='{nohp}'")
    driver.execute_script(f"document.getElementById('noTelp').value='{nohp}'")
    # driver.find_element(by=By.ID, value="email").send_keys(mailnesia)
    # driver.find_element(by=By.ID, value="noTelp").send_keys(nohp)
    driver.find_element(by=By.CSS_SELECTOR, value="#psw").send_keys('123456')
    driver.find_element(by=By.CSS_SELECTOR, value="#rePsw").send_keys('123456')
    driver.execute_script(f"document.getElementById('noTelp').value='{nohp}'")

    # input captcha
    promptedCaptcha = promptCaptcha(driver, "#captchaImage", "./djponline/workaround/collection3")
    driver.execute_script(f"document.getElementById('captcha').value='{promptedCaptcha}'")
    # return ''

    time.sleep(1)
    # driver.find_element(by=By.ID, value="btnVerifikasi").click()
    perform_actions(driver, Keys.ENTER)

    waitUntil(driver, "#swal2-content", 2)
    aktivasiConfirm = driver.execute_script("return document.querySelector('#swal2-content').textContent")
    print(aktivasiConfirm)

    while True:
        print('waiting if link is sent...')
        if includeText("berhasil dilakukan", aktivasiConfirm):
            break
        else:
            time.sleep(2)
            continue

    print('going to mailnesia..')

    emailID = mailnesia[:-14]
    try:
        ## new window
        driver.execute_script('''window.open("","_blank");''')

        # driver.execute_script('window.open('');')
        driver.switch_to.window(driver.window_handles[1])

        driver.get(f"http://mailnesia.com/mailbox/{emailID}")

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


        # wait until
        waitUntil(driver, ".emailheader", 2)
        # Textid = driver.find_elements_by_css_selector('.emailheader')[0].get_attribute('id') 
        Textid = driver.find_elements(by=By.CSS_SELECTOR, value=".emailheader")[0].get_attribute('id')
        # latestMail = driver.find_elements_by_css_selector('.emailheader td:nth-child(4)')[0]
        latestMail = driver.find_elements(by=By.CSS_SELECTOR, value=".emailheader td:nth-child(4)")[0]
        textTitle = latestMail.get_attribute("textContent")

        print('element located!')

        print('text Content :', textTitle)
        print('element id is', Textid)

        # test if lupa password
        a = textTitle.find('Aktivasi')

        if int(a) > -1:
            # click #emailbody_(id)
            driver.execute_script(f"document.getElementById({str(Textid)}).click()")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1]) # in case ads pop up
            print('back to DJP online...')
            driver.execute_script("document.querySelector('.es-button-border>a:nth-child(1)').click()")
            time.sleep(1)
            # waitUntil(driver, "#pswBaru", 2)

            # driver.find_element(by=By.CSS_SELECTOR, value="#pswBaru").send_keys('123456')
            # # driver.find_element_by_id("pswBaru").send_keys('123456')
            # driver.find_element(by=By.CSS_SELECTOR, value="#rePswBaru").send_keys('123456')
            # # driver.find_element_by_id("rePswBaru").send_keys('123456')

            # captchLupaPass = promptCaptcha(driver, "#captchaImage", "./djponline/workaround/collection3")
            # driver.execute_script(f"document.getElementById('captcha').value='{captchLupaPass}'")

            # driver.find_element_by_css_selector("#captcha").send_keys(captchLupaPass)
            # driver.find_element(by=By.CSS_SELECTOR, value="#captcha").send_keys(captchLupaPass)
            # # driver.find_element_by_css_selector("#btnVerifikasi").click()
            # driver.find_element(by=By.CSS_SELECTOR, value="#btnVerifikasi").click()
            time.sleep(1)
            waitUntil(driver, ".swal2-success-ring", 2)
            aktivasiResult = driver.execute_script("return document.querySelector('#swal2-content').textContent")
            print(aktivasiResult)
            closeTabs(driver)
            return f'result : {aktivasiResult}'
        else:
            print('password reset mail is not found!')
            return 'email not found!'
    except Exception as err:
        print(f"error : {err}")
        return f'error {str(err)}'