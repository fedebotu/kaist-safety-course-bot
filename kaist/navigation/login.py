from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def portal_login(driver, config, timeout=60):
    """Login into KAIST portal"""
    # Click OK button
    try:
        button = driver.find_element(by='css selector', value='.button .c_button .s_button')
        button.click()
    except: pass

    while True:
        
        if config.get('automatic_login', False) == True:
            try:
                print('Automatic login')
                driver.find_element(by='id', value='IdInput').send_keys(config['username'])
                button = driver.find_element(by='xpath', value='//input[@type="submit" and @value="간편 인증"]')
                button.click()
                print('Authenticate login with your phone. Alternatively, you can use the opened browser to navigate.')
                wait = WebDriverWait(driver, timeout=timeout, poll_frequency=1)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[ contains (text(), '간편인증이 진행중입니다')]")))
                print("Waiting for login... Will timeout after `timeout` seconds")
                wait.until_not(EC.element_to_be_clickable((By.XPATH, "//*[ contains (text(), '간편인증이 진행중입니다')]")))
                return
            except: 
                print('Automatic login failed. Trying manual login...')
                pass
        
        # Default behavior
        print('Manual login')
        print('Please login manually. You can use the opened browser to navigate the page.')
        WebDriverWait(driver, timeout=timeout, poll_frequency=1).until(EC.element_to_be_clickable((By.ID, 'IdInput')))
        # print('Login complete')
        return
    
