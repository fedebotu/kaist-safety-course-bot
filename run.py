"""
# KAIST Safety Course Automatic Viewer

This script makes viewing the (quite annoying) lab safety videos automatic, so you don't have to click 
many times on the videos that you need to see to complete the course :D

## NOTE
The scope of these scripts is NOT to disregard lab safety, which is extremely important for researchers! 
The purpose is mainly "for fun" (also don't you feel like a chad _cheating the system_)?
On a serious note, most people just find it annoying having to listen to
the courses they are not interested in so they skip them manually.
The exam can just be passed by failing the first time and completing the answers after knowing the results. 
So my question is: does this make sense? Why not just automate this tedious
and - for most - useless time-wasting process?
For any questions or complaints I will be available :)
PS: I'm not responsible for inappropriate use of this software of course ;)
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from kaist.video import watch_lessons, page_to_functions
from kaist.quiz import run_quiz
from kaist.login import portal_login
from kaist.config import input_config
from kaist.common import save_debug, check_education_end


def main():
    # Configuration
    config = input_config()

    # Call the driver and page
    driver = webdriver.Chrome(service=Service(config['driver_path']))
    driver.get(config['target_webpage'])

    try:
        # Login into KAIST
        portal_login(driver, config['username'])

        # Maximize window and open safety course page
        print('Waiting for the button to be visible... You may need to maximize the window')
        driver.maximize_window()
        WebDriverWait(driver, timeout=60, poll_frequency=1).until(EC.element_to_be_clickable((By.ID, 'eduGo')))
        button = driver.find_element(by='id', value='eduGo') # click button to go to page
        button.click()

        # Close popup
        windows = driver.window_handles
        driver.switch_to.window(windows[1]) # switch to popup window
        WebDriverWait(driver, timeout=60, poll_frequency=1).until(EC.element_to_be_clickable((By.ID, 'main_popup_0_close')))
        button = driver.find_element(by='id', value='main_popup_0_close') # click button to go to page
        button.click()
        driver.switch_to.window(windows[0]) # switch back after closing

        # Driver call
        driver.switch_to.window(driver.window_handles[1]) # switch to other window
        js = f"fn_movePage('{page_to_functions['마이페이지']}')"
        driver.execute_script(js)

        if not check_education_end(driver, config['video_id']):
            # Watch lessons
            print(f"Starting to watch video number {config['video_id']}...")
            watch_lessons(driver, config['video_id'], config['mute_video'])

            # Automated quiz
            if config['answer_quiz']:
                print(f"Answering quiz automatically...")
                run_quiz(driver)
        
    except Exception as e:
        print('An exception occurred during the program run:\n {}\nSaving debug.html...'.format(e))
        save_debug(driver)

    input("Done! Press ENTER to exit...")

if __name__ == "__main__":
    main()