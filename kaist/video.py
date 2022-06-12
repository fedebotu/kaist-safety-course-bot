from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from kaist.common import alert_accept

# This dictionary of functions lets you navigate in the menu with Javascript calls
page_to_functions = {'연구실 안전관리': "5c5a4661-37b3-4632-bbbb-e2413af45ff5",
                        '연구실 안전교육': "e416bcdf-2c66-4422-ad90-299c132d7a0d",
                        '가스': "d045cbec-63c7-4c53-83de-02512eca3182",
                        '화학물질': "177ad3d5-3866-4faf-8808-c171085417e0",
                        '마이페이지': "af97f864-2dcc-47b9-a7d2-35ee3e7d9627",
                        '시스템관리': "5a83c6c0-aa67-4dd3-8933-3be5d34c027c"}

                            
def mute(driver):
    """Mute embedded videos"""
    button = driver.find_element(by='id', value="vol")
    if button.get_attribute('onclick') == 'labEducation_mute()':
        button.click()


def watch_lessons(driver, video_id=0, mute_video=True):
    """Watch all the lessons for a given video id"""

    # Open course video corresponding to button id
    try:
        wait = WebDriverWait(driver, timeout=60, poll_frequency=1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[ contains (text(), '강의듣기')]")))
        buttons = driver.find_elements(by='xpath', value="//*[ contains (text(), '강의듣기')]")
        buttons[video_id].click()
    except:
        print("The video is either already open or the page is wrong")

    try:
        current_video = int(driver.find_element(by='id', value="nowPage").text)
        last_video = int(driver.find_element(by='id', value="lastPage").text)
    except:
        return # if there is an error, it means that the video should be over

    while current_video <= last_video:
        try:
            current_video = int(driver.find_element(by='id', value="nowPage").text) 
        except:
            alert_accept(driver, timeout=3) # accept the alert: this should happen when we finished watching
            break

        print(f"Watching video {current_video}/{last_video}...")

        if mute_video: mute(driver) # video volume muting

        # Wait until the next button is working
        while driver.find_element(by='xpath', value="//*[ contains (text(), 'NEXT')]").get_attribute('disabled') is not None:
            time.sleep(1)
            current_time = driver.find_element(by='id', value="currentTime").text
            total_time = driver.find_element(by='id', value="totalTime").text
            print(f"Progress: {current_time}/{total_time}", end='\r')

        try:
            # Next video
            button = driver.find_element(by='xpath', value="//*[ contains (text(), 'NEXT')]")
            button.click()
        except:
            # If we cannot click next anymore, we reached the quiz
            break