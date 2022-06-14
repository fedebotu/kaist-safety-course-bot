import PySimpleGUI as sg
import webbrowser
import sys

from kaist.config import DEFAULT_CONFIG
from kaist.config import load_config, dump_config
from kaist.gui.utils import get_config_from_values, load_config_to_window
from kaist.navigation.main import run_main
from kaist.utils import ThreadWithException
from kaist.gui.logo import LOGO_B64

DEFAULT_THEME = 'Reddit'
DEFAULT_FONT = 'Calibri 11'
APP_VERSION = "0.1.0"
GITHUB_PAGE = "https://github.com/fedebotu/kaist-safety-course-bot"
ABOUT_TEXT = 'This bot makes viewing the (quite annoying) lab safety videos automatic, so you don`t have to click many times on the videos that you need to see to complete the course. Also, considering that as of the time of writing the quiz can not be failed, the bot can additionally complete it too :D.'
HELP_TEXT = "We will be using Chrome, so the Chromedriver needs to be downloaded and loaded from the interface.\nMake sure your Chrome version corresponds to the Chromedriver's one!\nYou may also want to check out the following links."


def show_about_page(window):
    """Show about page"""
    window.Hide()
    _layout = [[sg.Text("KAIST Safety Course Bot", font="Calibri 16")],[sg.Text(ABOUT_TEXT,font=DEFAULT_FONT, size=(50, 6))],
    [sg.Text(f"Application version: {APP_VERSION}",font=DEFAULT_FONT)],
    # [sg.Text("Downloaded from: ",font=DEFAULT_FONT)],
    [sg.Button("Back",font=DEFAULT_FONT),
    sg.Button("GitHub",font=DEFAULT_FONT)]]
    _window = sg.Window('About',_layout,debugger_enabled=False, icon=LOGO_B64)
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


def show_help_page(window):
    """Show help page"""
    window.Hide()
    _layout = [[sg.Text(HELP_TEXT,font=DEFAULT_FONT, enable_events=True)],
    [sg.Button("Back",font=DEFAULT_FONT),
    sg.Button("More Help on GitHub",font=DEFAULT_FONT), 
    sg.Button("Download Chromedriver",font=DEFAULT_FONT),
    sg.Button("KAIST Safety Course Website",font=DEFAULT_FONT)]
    ]
    _window = sg.Window('Help',_layout,debugger_enabled=False, icon=LOGO_B64)
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


def main_page():
    """Main page"""
    config = load_config()
    sg.theme(DEFAULT_THEME)

    layout = [
        [sg.Text('Settings', size=(30, 1), font=("Calibri", 18))],
        [sg.Text('KAIST Username')],
        [sg.InputText(config['username'], key='username', tooltip='Your KAIST username.\nWe will use this to access the webpage')],
        [sg.Text('Video ID')],
        [sg.InputText(config['video_id'], key='video_id', tooltip='The video number (starting from 0) you want to watchℕnThese videos are marked with `정기`')],
        [sg.Text('Target webpage')],
        [sg.InputText(config['target_webpage'], key='target_webpage', tooltip='Change only if you cannot access the default URL')],
        [sg.CBox('Answer quiz', key='answer_quiz', default=True, tooltip="Answer the quiz automatically.\nIMPORTANT: we assume there is no penalty for failing the test!"), 
            sg.CBox('Mute videos', key='mute_video', default=True, tooltip="Set the volume to 0 while watching the videos")],
        [sg.Text('Driver Path')],
        [sg.Text('Choose folder', size=(15, 1), justification='right'),
         sg.InputText(config['driver_path'], key='driver_path'), sg.FolderBrowse(tooltip='Your chromedriver path\n(go to "Help" section for more info)')],
        [sg.Button('Save Configuration', key='Save'), sg.Button('Load Saved Configuration', key='Load'), sg.Button('Load Default Configuration', key='Reload')],
        [sg.Text('Debug window')],
        [sg.Multiline("", size=(80, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='STDOUT', disabled=True)],
        [sg.Button('Run', tooltip='Run program with current configuration'), sg.Button('Stop', tooltip='Stop current run'), sg.Button('Help'), sg.Button('About'), sg.Button('Exit')],
        # [sg.ProgressBar(max_value=100, key='bsar', metadata=5)],
    ]

    window = sg.Window('KAIST Safety Course Bot', layout, icon=LOGO_B64)


    thread = None
    while True:
        event, values = window.read()
        if event == 'Run':
            config = get_config_from_values(values)
            print("Starting run...")
            thread = ThreadWithException('Main', target=run_main,  args=config)
            thread.start()
        if event == 'Stop':
            if thread:
                thread.raise_exception()
                # thread.join()
                print("Run was manually terminated")
                thread = None
            else:
                print("No thread is currently running")

        if event == 'Load':
            config = load_config()
            window = load_config_to_window(window, values, config)
            print("Loaded saved configuration")

        if event == 'Reload':
            window = load_config_to_window(window, values, DEFAULT_CONFIG)
            print("Reloaded default configuration")

        if event == 'Save':
            config = get_config_from_values(values)
            print("The configuration has been saved")
            dump_config(config)

        if event == 'About':
            show_about_page(window)
        if event == 'Help':
            show_help_page(window)
        if event == ('Exit'):
            break

    window.close()


if __name__ == "__main__":
    # sg.preview_all_look_and_feel_themes()
    main_page()