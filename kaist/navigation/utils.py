from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def check_education_end(driver, video_id=0):
    """Check if the education on the video is over"""
    def _element_available(driver):
        if driver.find_elements(By.CLASS_NAME, "edu_cate") != []: 
            return True
        return False

    wait = WebDriverWait(driver, timeout=60, poll_frequency=1)
    wait.until(_element_available)
    edu_containers = driver.find_elements(By.CLASS_NAME, "edu_cate")
    els = edu_containers[video_id].find_element(By.XPATH, "../..")
    lesson_title = edu_containers[video_id].find_element(By.XPATH, "./..").text
    print(20*'='+f'\nLessons with ID {video_id}:\n {lesson_title}\n'+20*'=')
    if els.get_attribute("class") == 'edu_end':
        print("Lessons with ID {video_id} have been completed! :D")
        return True
    return False


def alert_accept(driver, timeout=10):
    """Accept alert if there is one"""
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
    except Exception:
        pass
    

def save_debug(driver, filename='debug.html'):
    """Save debug page"""
    with open(filename, 'w') as f:
        f.write(driver.page_source)