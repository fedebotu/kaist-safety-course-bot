from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def portal_login(driver, username):
    """Login into KAIST portal"""
    # Click OK button
    try: driver.find_element(by='css selector', value='.button .c_button .s_button').click()
    except: pass

    try: 
        driver.find_element(by='id', value='IdInput').send_keys(username)
        button = driver.find_element(by='xpath', value='//input[@type="submit" and @value="간편 인증"]')
        button.click()
        print('Authenticate login with your phone. Alternatively, you can use the opened browser to navigate.')
    except: 
        pass
    wait = WebDriverWait(driver, timeout=60, poll_frequency=1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[ contains (text(), '간편인증이 진행중입니다')]")))
    print("Waiting for login... Will timeout after 60 seconds")
    wait.until_not(EC.element_to_be_clickable((By.XPATH, "//*[ contains (text(), '간편인증이 진행중입니다')]")))