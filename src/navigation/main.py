from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from src.navigation.video import watch_videos
from src.navigation.login import portal_login
from src.navigation.utils import save_debug, alert_accept, click_all_until_done


def run_main(config, driver):
    """Main program function: take existing config and run"""

    try:
        # Call the driver and page
        driver.get(config['target_webpage'])

        # Login into KAIST
        portal_login(driver, config)

        # Maximize window and open safety course page
        print('Waiting for the button to be visible... You may need to maximize the window')
        driver.maximize_window()
        WebDriverWait(driver, timeout=60, poll_frequency=1).until(EC.element_to_be_clickable((By.ID, 'eduGo')))
        button = driver.find_element(by='id', value='eduGo') # click button to go to page
        button.click()

        # Close popup
        windows = driver.window_handles
        driver.switch_to.window(windows[1]) # switch to popup window
        alert_accept(driver, timeout=10)

        # Close all popups
        click_all_until_done(driver, by=By.XPATH, value="//*[contains(text(), '닫기')]")

        # Open My Page and close all possible alerts
        print("Opening My Page...")
        button = driver.find_element(by=By.XPATH, value="//*[contains(text(), '마이페이지')]")
        button.click()
        alert_accept(driver, timeout=5)

        # Watch videos sequentially
        print("Select video lessons to watch and open the video stream of one. I will watch the rest for you! Waiting for video...")
        watch_videos(driver, config)
        
        print("Done!")
        
    except Exception as e:
        print(f"{e}\nException occurred during program run\nSaving debug to {config['debug_path']}...")
        save_debug(driver, config['debug_path'])
        print("==============\nOuch, an error occurred! =(\nReload Driver to restart!\n==============")

    finally:
        print("Program finished!")
        # print('Program finished!\nPress Stop or close browser windows to exit...')
        # while True:
        #     time.sleep(3)


