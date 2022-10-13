from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.navigation.utils import alert_accept


def click_accept(driver):
    """Click accept button if there is one"""
    try:
        buttons = driver.find_elements(by='xpath', value="//span[ contains (text(), '확인')]")
        buttons[0].click() # lazy to find the exact pattern, just got the list here
    except:
        pass
    alert_accept(driver)


def click_retry(driver):
    """Click retry button if there is one"""
    try:
        driver.find_element(by='xpath', value="//span[ contains (text(), '다시풀기')]").click()
    except:
        pass
    alert_accept(driver)
 

def first_run_quiz(driver):
    """First dry run: collect answers database and select the first ones only"""
    questions = driver.find_elements(by='css selector', value="label[class*='sbux-uuid-txtQuiz']")
    num_questions = len(questions)

    questions_answers = []

    # Get answers for each question
    for qnum in range(1, num_questions+1, 1):
        question = driver.find_element(by='id', value="txtQuiz{}".format(qnum)).text
        answers = []
        radio_buttons = driver.find_elements(by='css selector', value='.sbux-uuid-labEducationMng_rdoQuiz{}'.format(qnum-1))
        num_answers = len(radio_buttons) # weird numbering

        # Answer selection
        wait = WebDriverWait(driver, timeout=30, poll_frequency=1)
        wait.until(EC.element_to_be_clickable(radio_buttons[0]))
        radio_buttons[0].click() 
        for anum in range(num_answers):
            answer = driver.find_element(by='id', value='labEducationMng_rdoQuiz{}_{}'.format(qnum, anum))
            answer_text = answer.get_attribute('text')
            answer_checked = True if answer.get_attribute('checked') is not None else False
            answer_iswrong = 'unknown'
            answers.append({'number': anum, 'text': answer_text, 'checked': answer_checked, 'iswrong': answer_iswrong})
        questions_answers.append({'question': question, 'answers': answers})
    return questions_answers


def adjust_answers(driver, questions_answers):
    """Collect data about the previous run:"""
    num_questions = len(questions_answers)
    # Get answers for each question
    for qnum in range(1, num_questions+1, 1):
        question = driver.find_element(by='id', value="txtQuiz{}".format(qnum))
        wrong = question.get_attribute('style') != '' # answer is wrong if colored in red (so has a style)
        # driver.find_element(by='id', value="txtQuiz{}".format(qnum))

        radio_buttons = driver.find_elements(by='css selector', value='.sbux-uuid-labEducationMng_rdoQuiz{}'.format(qnum-1))
        num_answers = len(radio_buttons) # weird numbering

        _answered = False
        for anum in range(num_answers):
            answer = driver.find_element(by='id', value='labEducationMng_rdoQuiz{}_{}'.format(qnum, anum))
            answer_checked = True if answer.get_attribute('checked') is not None else False

            if wrong and not _answered and questions_answers[qnum-1]['answers'][anum]['iswrong'] == 'unknown' and not answer_checked:
                radio_buttons[anum].click() 
                _answered = True
            elif wrong and not _answered:
                questions_answers[qnum-1]['answers'][anum]['iswrong'] = True

            answer = driver.find_element(by='id', value='labEducationMng_rdoQuiz{}_{}'.format(qnum, anum))
            answer_checked = True if answer.get_attribute('checked') is not None else False

            if not wrong and answer_checked:
                questions_answers[qnum-1]['answers'][anum]['iswrong'] = False
    return questions_answers


def retry_quiz(driver, questions_answers):
    """Retry quiz with the answers collected in the previous run"""
    num_questions = len(questions_answers)
    # Get answers for each question
    for qnum in range(1, num_questions+1, 1):

        radio_buttons = driver.find_elements(by='css selector', value='.sbux-uuid-labEducationMng_rdoQuiz{}'.format(qnum-1))
        num_answers = len(radio_buttons) # weird numbering

        # Answer selection 
        for anum in range(num_answers):
            answer = questions_answers[qnum-1]['answers'][anum]
            if answer['iswrong'] == True:
                continue
            elif answer['iswrong'] == False:
                radio_buttons[anum].click() 
                break
            elif answer['iswrong'] == 'unknown':
                radio_buttons[anum].click() 
                break
    return


def run_quiz(driver):
    """
    Run the quiz iteratively
    We assume that the quiz does not incur any penalty for the retries!
    """
    try: driver.find_element(by='xpath', value="//*[ contains (text(), 'QUIZ')]").click()
    except: pass
    questions_answers = first_run_quiz(driver)
    click_accept(driver)
    quiz_is_complete = False

    try:
        while not quiz_is_complete:
            # Adjust answers based on the first quiz
            questions_answers = adjust_answers(driver, questions_answers)
            click_retry(driver)

            # Re-Input answers
            retry_quiz(driver, questions_answers)
            click_accept(driver)
        
    except Exception as e:
        print('An exception occurred during the quiz run:\n {}'.format(e))