from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from src.navigation.utils import alert_accept, save_debug


def watch_videos(driver, config):               
    """Watch videos automatically with options for speeding up and muting"""
    retries = 0
    while True:
        try:
            driver.switch_to.parent_frame()
            button_play = driver.find_elements(by=By.CLASS_NAME, value="btn_WF_VpPlay")
            button_stop = driver.find_elements(by=By.CLASS_NAME, value="btn_WF_VpStop")
            button_quiz = driver.find_elements(by=By.CLASS_NAME, value="btn_WF_VpConQuiz")
            if len(button_play) > 0 or len(button_stop) > 0:
                if len(button_quiz) > 0:
                    try:
                        button_quiz[0].click()
                        print("For now, you will need to answer the quiz yourself! Perhaps I will automate it someday ;)")
                    except:
                        print("Tried clicking quiz button, but failed. Human, please try!")
                        pass
                    finally:
                        break

                # We have the video screen open
                # Check if the video is playing, if not play it
                button = driver.find_elements(by=By.CLASS_NAME, value="btn_WF_VpSound")
                if len(button) > 0 and config['mute_video']:
                    print("Turning off sound")
                    button[0].click()
                if len(button_play) > 0:
                    print("Playing video")
                    button_play[0].click()
                    driver.execute_script(f'''document.querySelector('video').playbackRate = {config['playback_rate']};''')
                    
            # else:
            #     # we have the video screen closed
            #     # print("No video screen detected! Please open video first")
            #     pass

        except Exception as e:
            retries += 1
            # alert_accept(driver, timeout=3)
            WebDriverWait(driver, 10).until_not(EC.alert_is_present(), "Popup alert found, please deal with it human!")
            if retries > config['max_retries']:
                print("Too many retries, giving up!\nException: ", e)
                save_debug(driver, config['debug_path'])
                print("==============\nOuch, an error occurred! =(\nReload Driver to restart!\n==============")
                break

        time.sleep(3)
