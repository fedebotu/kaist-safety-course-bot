import PySimpleGUI as gui
import webbrowser
import sys
import darkdetect

from kaist.config import DEFAULT_CONFIG
from kaist.config import load_config, dump_config
from kaist.gui.utils import get_config_from_values, load_config_to_window
from kaist.navigation.main import run_main
from kaist.navigation.utils import save_debug
from kaist.utils import ThreadWithException
from kaist.navigation.webdriver import setup_webdriver
from kaist.gui.images import LOGO_B64, BLUE_DOTS_B64
from kaist.gui.button import RoundedButton

DEFAULT_THEME = 'Reddit'
DEFAULT_FONT = 'Calibri 12'
APP_VERSION = "1.0.0"
GITHUB_PAGE = "https://github.com/fedebotu/kaist-safety-course-bot"
ABOUT_TEXT = 'This bot makes viewing the (quite annoying) lab safety videos automatic, so you don`t have to click many times on the videos that you need to see to complete the course. Also, considering that as of the time of writing the quiz can not be failed, the bot can additionally complete it too :D.'
HELP_TEXT_CHROMEDRIVER = "We will be using Chrome, so the Chromedriver needs to be downloaded and loaded from the interface. Make sure your Chrome version corresponds to the Chromedriver's one!"
HELP_TEXT_VIRUS = "Windows may flag the program as a virus since it contains browser automation. But hey, guess what, it isn`t :) Try to temporarily deactivate or make an exception in Windows Defender."
HELP_TEXT_OTHER = "Did you encounter another bug? Try visiting the Github page or contact us!"

# Set theme
if not darkdetect.isDark():
    gui.theme("LightGrey")
    BACKGROUND_COLOR = "#232020"
    INPUT_BACKGROUND_COLOR = '#ADD8E6'
    gui.theme_background_color(BACKGROUND_COLOR)
    gui.theme_text_element_background_color(BACKGROUND_COLOR)
    gui.theme_text_color("White")
    gui.theme_button_color((BACKGROUND_COLOR, INPUT_BACKGROUND_COLOR))
    gui.theme_input_background_color(INPUT_BACKGROUND_COLOR)
    gui.theme_input_text_color('#000000')
    TAB_TEXT_COLOR="Black"
else:
    BACKGROUND_COLOR = "#FAFAFA"
    INPUT_BACKGROUND_COLOR = '#0079D3'
    TAB_TEXT_COLOR="White"
    gui.theme("LightGrey")


def main_page():
    """Main page"""
    config = load_config()

    layout_tab1 = [
        [gui.Text('Main Settings', font='Calibri 14')],
        [gui.Text('Tip: you can hover over the elements to get more information about them')],
        [gui.Text('Video ID', font=DEFAULT_FONT)],
        [gui.Spin([x for x in range(0, 10, 1)], initial_value=config['video_id'], key='video_id', tooltip='The video number (starting from 0) you want to watch\nThese videos are marked with `정기`')],
        [gui.Text('Answer Quiz', font=DEFAULT_FONT)],
        [gui.CBox('Answer quiz', key='answer_quiz', background_color=BACKGROUND_COLOR, default=True, tooltip="Answer the quiz automatically.\nIMPORTANT: we assume there is no penalty for failing the test!")], 
        [gui.Text('Mute videos', font=DEFAULT_FONT)],
        [gui.CBox('Mute videos', key='mute_video', background_color=BACKGROUND_COLOR, default=True, tooltip="Set the volume to 0 while watching the videos")],]

    layout_tab2 = [
        [gui.Text('[Optional] KAIST Username')],
        [gui.InputText(config['username'], key='username', tooltip='Your KAIST username.\nWe will use this to access the webpage if supplied')],
        [gui.Text('[Optional] Automatic Login with Username')],
        [gui.CBox('Automatic login', key='automatic_login', background_color=BACKGROUND_COLOR, default=False, tooltip="Login automatically to the KAIST website.\nIf you don't want to login, you can leave this unchecked")],
        [gui.Text('[Optional] Driver Path')],
       [gui.Text('Choose File', size=(15, 1), justification='right'),
            gui.InputText(config['driver_path'], key='driver_path'), gui.FileBrowse(tooltip='Your chromedriver path (Windows: chromedriver.exe)\n(go to "Help" section for more info)')],
        [gui.Text('[Optional] Target webpage')],
        [gui.InputText(config['target_webpage'], key='target_webpage', tooltip='Change only if you cannot access the default URL')],
        [gui.Text('Configuration')],
        [RoundedButton('Save', key='Save'), RoundedButton('Load', key='Load'), RoundedButton('Load Default', key='Reload')], 
    ]

    layout_tab3 = [
        [gui.Text("KAIST Safety Course Bot", font="Calibri 18")],
        [gui.Column([[gui.Image(data=LOGO_B64, size=(150,150), subsample=(5))]], justification='center')],
        [gui.Text(ABOUT_TEXT, size=(80, 6))],
        [gui.Text(f"Application version: {APP_VERSION}",font=DEFAULT_FONT)],
        [RoundedButton("GitHub")],
    ]

    layout_tab4 = [[gui.Text('Chromedriver Installation', font='Calibri 16')],
        [gui.Text(HELP_TEXT_CHROMEDRIVER, size=(80, 4),enable_events=True)],
        [gui.Text('Virus Detection',font='Calibri 16')],
        [gui.Text(HELP_TEXT_VIRUS, size=(80, 4), enable_events=True)],
        [gui.Text('Other Bugs',font='Calibri 16')],
        [gui.Text(HELP_TEXT_OTHER, size=(80, 4), enable_events=True)],
        [RoundedButton("Help on GitHub"), 
        RoundedButton("Safety Course Website")]
        ]

    layout = [[gui.TabGroup([[gui.Tab('Main', layout_tab1, title_color='Blue',
                                tooltip='Main settings', background_color=BACKGROUND_COLOR),
                             gui.Tab('Advanced Settings', layout_tab2, title_color='Blue',
                                tooltip='Extra stuff you might want to look into', background_color=BACKGROUND_COLOR),
                            gui.Tab('Help', layout_tab4, title_color='Blue',
                                tooltip='For quick help', background_color=BACKGROUND_COLOR),
                             gui.Tab('About', layout_tab3, title_color='Blue',
                                tooltip='About page and details', background_color=BACKGROUND_COLOR),
                            ]], background_color=BACKGROUND_COLOR, tab_background_color=INPUT_BACKGROUND_COLOR, title_color=TAB_TEXT_COLOR)],
    
            [[gui.Text('Debug window', font=("Calibri", 18))],
            [gui.Multiline("", size=(80, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='STDOUT', disabled=True)],
            [RoundedButton('Run', tooltip='Run program with current configuration'), RoundedButton('Load Driver', tooltip='Install webdriver for selected browser'), 
             RoundedButton('Debug', tooltip='Save debug'), RoundedButton('Stop', tooltip='Stop current run'), RoundedButton('Exit')],]]


    window = gui.Window('KAIST Safety Course Bot', layout, icon=LOGO_B64)


    thread = None    
    driver = None
    while True:
        event, values = window.read(timeout=10)

        if event == 'Run':
            config = get_config_from_values(values)
            if driver is None:
                if 'driver_thread' in locals(): # check if this was instantiated before
                    driver = driver_thread.return_value
                    if driver is None:
                        print("Wait for driver installation to finish!")
                    else:
                        print('Starting run...')
                        thread = ThreadWithException(target=run_main,  args=(config, driver))
                        thread.start()
                else:
                    print("Load driver first!")

        if event == 'Load Driver':
            config = get_config_from_values(values)
            driver = None # reset driver
            print(f"Setting up webdriver for {config['browser']}...")
            driver_thread = ThreadWithException(target=setup_webdriver, args=(config['browser'],))
            driver_thread.start()
            
        if event == 'Debug':
            config = get_config_from_values(values)
            if driver is not None:
                print('Saving debug page...')
                save_debug(driver, config['debug_path'])

        elif event == 'Stop':
            if thread:
                thread.raise_exception()
                print("Run was manually terminated")
                thread = None
            else:
                print("No thread is currently running")
        elif event == 'Load':
            config = load_config()
            window = load_config_to_window(window, values, config)
            print("Loaded saved configuration")
        elif event == 'Reload':
            window = load_config_to_window(window, values, DEFAULT_CONFIG)
            print("Reloaded default configuration")
        elif event == 'Save':
            config = get_config_from_values(values)
            print("The configuration has been saved")
            dump_config(config)
        elif event == "More Help on GitHub":
            webbrowser.open(GITHUB_PAGE,2)
        elif event == "Download Chromedriver":
            webbrowser.open("https://chromedriver.chromium.org/downloads",2)
        elif event == "KAIST Safety Course Website":
            webbrowser.open("https://safety.kaist.ac.kr/portal/main.do",2)
        elif event == gui.WIN_CLOSED or event == 'Exit':
            break

    print("Closing remaing threads and windows...")
    if thread: thread.raise_exception()
    if driver: 
        # driver.close()
        driver.quit()
    window.close()
    exit()



if __name__ == "__main__":
    # gui.preview_all_look_and_feel_themes()
    main_page()