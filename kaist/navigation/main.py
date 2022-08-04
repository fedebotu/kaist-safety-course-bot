from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from kaist.navigation.video import watch_lessons, page_to_functions
from kaist.navigation.quiz import run_quiz
from kaist.navigation.login import portal_login
from kaist.navigation.utils import save_debug, check_education_end
from kaist.utils import ThreadWithException


def run_main(config, driver):
    """Main program function: take existing config and run"""

    # Call the driver and page
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
        print("Done!")
        
    except Exception as e:
        print(f"An exception occurred during the program run:\n {e}\nSaving debug to {config['debug_path']}...")
        save_debug(driver, config['debug_path'])

    print('Program finished!\nPress Stop or close browser windows to exit...')
    while True:
        time.sleep(3)


# class MainApplication(ThreadWithException):
#     """
#     Main application class
    
#     Args:
#         config (dict): configuration dictionary
#     """
#     def __init__(self, config):
#         super(MainApplication, self).__init__(None, None)
#         self.driver = setup_webdriver(config['browser'])
#         self.target = run_main
#         self.args = config, self.driver

    # def main(self):
    #     """Run the application"""
    #     thread = ThreadWithException(target=self.run_main)
    #     thread.start()

