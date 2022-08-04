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
DEFAULT_FONT = 'Calibri 11'
APP_VERSION = "0.2.0"
GITHUB_PAGE = "https://github.com/fedebotu/kaist-safety-course-bot"
ABOUT_TEXT = 'This bot makes viewing the (quite annoying) lab safety videos automatic, so you don`t have to click many times on the videos that you need to see to complete the course. Also, considering that as of the time of writing the quiz can not be failed, the bot can additionally complete it too :D.'
HELP_TEXT_CHROMEDRIVER = "We will be using Chrome, so the Chromedriver needs to be downloaded and loaded from the interface.\nMake sure your Chrome version corresponds to the Chromedriver's one!"
HELP_TEXT_VIRUS = "Windows may flag the program as a virus since it contains browser automation.\nBut hey, guess what, it isn`t :)\nTry to temporarily deactivate or make an exception in Windows Defender."
HELP_TEXT_OTHER = "Did you encounter another bug? Try visiting the Github page or contact us!"

# Set theme

if not darkdetect.isDark():
    gui.theme("LightGrey")
    BACKGROUND_COLOR = "#232020"
    gui.theme_background_color(BACKGROUND_COLOR)
    gui.theme_text_element_background_color("#232020")
    gui.theme_text_color("White")
    gui.theme_button_color(('#232020', '#ADD8E6'))
    gui.theme_input_background_color('#ADD8E6')
    gui.theme_input_text_color('#000000')
else:
    BACKGROUND_COLOR = "White"
    gui.theme("LightGrey")


def show_about_page(window):
    """Show about page"""
    window.Hide()
    _layout = [[gui.Text("KAIST Safety Course Bot", font="Calibri 16")],
    [gui.Column([[gui.Image(data=LOGO_B64, size=(250,250), subsample=(3))]], justification='center')],
    [gui.Text(ABOUT_TEXT,font=DEFAULT_FONT, size=(50, 6))],
    [gui.Text(f"Application version: {APP_VERSION}",font=DEFAULT_FONT)],
    # [gui.Text("Downloaded from: ",font=DEFAULT_FONT)],
    [RoundedButton("Back",font=DEFAULT_FONT),
    RoundedButton("GitHub",font=DEFAULT_FONT)]]
    _window = gui.Window('About',_layout,debugger_enabled=False, icon=LOGO_B64)
    while True:
        event,values = _window.Read()
        if event is None:
            sys.exit(0)
        elif event == "Back":
            _window.Close()
            window.UnHide()
            break
        elif event == "GitHub":
            webbrowser.open(GITHUB_PAGE,2)
        if event == gui.WIN_CLOSED or event == 'Exit':
            break


def show_help_page(window):
    """Show help page"""
    window.Hide()
    _layout = [[gui.Text('Chromedriver Installation',font='Calibri 16')],
    [gui.Text(HELP_TEXT_CHROMEDRIVER,font=DEFAULT_FONT, enable_events=True)],
    [gui.Text('Virus Detection',font='Calibri 16')],
    [gui.Text(HELP_TEXT_VIRUS,font=DEFAULT_FONT, enable_events=True)],
    [gui.Text('Other Bugs',font='Calibri 16')],
    [gui.Text(HELP_TEXT_OTHER,font=DEFAULT_FONT, enable_events=True)],
    [RoundedButton("Back",font=DEFAULT_FONT),
    RoundedButton("More Help on GitHub",font=DEFAULT_FONT), 
    RoundedButton("Download Chromedriver",font=DEFAULT_FONT),
    RoundedButton("KAIST Safety Course Website",font=DEFAULT_FONT)]
    ]
    _window = gui.Window('Help',_layout,debugger_enabled=False, icon=LOGO_B64)
    while True:
        event, values = _window.Read()
        if event is None:
            sys.exit(0)
        elif event == "Back":
            _window.Close()
            window.UnHide()
            break
        elif event == "More Help on GitHub":
            webbrowser.open(GITHUB_PAGE,2)
        elif event == "Download Chromedriver":
            webbrowser.open("https://chromedriver.chromium.org/downloads",2)
        elif event == "KAIST Safety Course Website":
            webbrowser.open("https://safety.kaist.ac.kr/portal/main.do",2)
        if event == gui.WIN_CLOSED or event == 'Exit':
            break


def main_page():
    """Main page"""
    config = load_config()

    layout = [
        [gui.Text('Settings', size=(30, 1), font=("Calibri", 18))],
        [gui.Text('KAIST Username')],
        [gui.InputText(config['username'], key='username', tooltip='Your KAIST username.\nWe will use this to access the webpage')],
        [gui.Text('Video ID')],
        [gui.InputText(config['video_id'], key='video_id', tooltip='The video number (starting from 0) you want to watch\nThese videos are marked with `정기`')],
        [gui.Text('Target webpage')],
        [gui.InputText(config['target_webpage'], key='target_webpage', tooltip='Change only if you cannot access the default URL')],
        [gui.CBox('Answer quiz', key='answer_quiz', default=True, tooltip="Answer the quiz automatically.\nIMPORTANT: we assume there is no penalty for failing the test!"), 
            gui.CBox('Mute videos', key='mute_video', default=True, tooltip="Set the volume to 0 while watching the videos")],
        [gui.Text('Driver Path')],
        [gui.Text('Choose File', size=(15, 1), justification='right'),
         gui.InputText(config['driver_path'], key='driver_path'), gui.FileBrowse(tooltip='Your chromedriver path (Windows: chromedriver.exe)\n(go to "Help" section for more info)')],
        [RoundedButton('Save Configuration', key='Save'), RoundedButton('Load Saved Configuration', key='Load'), RoundedButton('Load Default Configuration', key='Reload')],
        [gui.Text('Debug window')],
        [gui.Multiline("", size=(90, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='STDOUT', disabled=True)],
        [RoundedButton('Run', tooltip='Run program with current configuration'), RoundedButton('WebDriver', tooltip='Install webdriver for selected browser'), 
        RoundedButton('Debug', tooltip='Save debug'), RoundedButton('Stop', tooltip='Stop current run'), RoundedButton('Help'), RoundedButton('About'), RoundedButton('Exit')],
        # [gui.ProgressBar(max_value=100, key='bsar', metadata=5)],
    ]

    layout_tab1 = [
        [gui.Text('KAIST Username')],
        [gui.InputText(config['username'], key='username', tooltip='Your KAIST username.\nWe will use this to access the webpage')],
        [gui.Text('Video ID')],
        [gui.InputText(config['video_id'], key='video_id', tooltip='The video number (starting from 0) you want to watch\nThese videos are marked with `정기`')],
        [gui.Text('Target webpage')],
        [gui.InputText(config['target_webpage'], key='target_webpage', tooltip='Change only if you cannot access the default URL')],
        [gui.CBox('Answer quiz', key='answer_quiz', default=True, tooltip="Answer the quiz automatically.\nIMPORTANT: we assume there is no penalty for failing the test!"), 
            gui.CBox('Mute videos', key='mute_video', default=True, tooltip="Set the volume to 0 while watching the videos")],
        [gui.Text('Driver Path')],]

    layout_tab2 = [
       [gui.Text('Choose File', size=(15, 1), justification='right'),
         gui.InputText(config['driver_path'], key='driver_path'), gui.FileBrowse(tooltip='Your chromedriver path (Windows: chromedriver.exe)\n(go to "Help" section for more info)')],
        [RoundedButton('Save Configuration', key='Save'), RoundedButton('Load Saved Configuration', key='Load'), RoundedButton('Load Default Configuration', key='Reload')], 
    ]

    layout = [[gui.Text('Settings', size=(30, 1), font=("Calibri", 18))],
                            [gui.TabGroup([[gui.Tab('Personal Details', layout_tab1, title_color='Red',
                                tooltip='Personal details', background_color=BACKGROUND_COLOR),
                             gui.Tab('Personal Details', layout_tab2, title_color='Blue',
                                tooltip='Personal details', background_color=BACKGROUND_COLOR)]], background_color=BACKGROUND_COLOR),],
    
        [[gui.Text('Debug window', font=("Calibri", 18))],
        [gui.Multiline("", size=(90, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='STDOUT', disabled=True)],
        [RoundedButton('Run', tooltip='Run program with current configuration'), RoundedButton('WebDriver', tooltip='Install webdriver for selected browser'), 
        RoundedButton('Debug', tooltip='Save debug'), RoundedButton('Stop', tooltip='Stop current run'), RoundedButton('Help'), RoundedButton('About'), RoundedButton('Exit')],]]

    
    # tab1_layout =  [[gui.T('This is inside tab 1')]]

    # tab2_layout = [[gui.T('This is inside tab 2')],
    #             [gui.In(key='in')]]
    # layout = [[gui.TabGroup([[gui.Tab('Tab 1', tab1_layout), gui.Tab('Tab 2', tab2_layout)]])],
    #             [gui.RButton('Read')]]
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
                    print("Install driver first!")

        if event == 'WebDriver':
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
        elif event == 'About':
            show_about_page(window)
        elif event == 'Help':
            show_help_page(window)
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