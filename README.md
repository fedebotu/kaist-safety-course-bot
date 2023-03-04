<div align="center">

# KAIST Safety Course Bot

[![Latest release](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/fedebotu/kaist-safety-course-bot/releases/download/v1.0.1/windows-kaist-safety-course-bot-v1.0.1.zip) [![Latest release](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/fedebotu/kaist-safety-course-bot/releases/download/v1.0.1/mac-kaist-safety-course-bot-v1.0.1.zip)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)






</div>

A bot for automatically completing the KAIST safety course.

> This bot makes viewing the (quite annoying) lab safety videos automatic, so you don't have to click many times on the videos that you need to see to complete the course. Also, considering that as of the time of writing the quiz can't be failed, the bot can additionally complete it too :D

**NOTICE (2022/10/13)**
> Due to changes in KAIST's website, the bot was upgrade and can now deal with the video viewing in the new website, while the quiz is still in the works
한국어판: [![en](https://img.shields.io/badge/lang-kor-blue.svg)](https://github.com/fedebotu/kaist-safety-course-bot/edit/main/README.ko.md)


<!--- [![ko](https://img.shields.io/badge/lang-ko-blue.svg)](file path will be here)--->

## App Screenshot

<p align="center">
  <img src="assets/app-screenshot.png" width = 40% alt="Image">
</p>

## Usage
First, choose you target courses in the [KAIST Safety Website](https://safety.kaist.ac.kr/main/main.do). Then:

- For Windows/Mac users:

1. From the [Release Page](https://github.com/fedebotu/kaist-safety-course-bot/releases/), download and run files that fit your operating system! **Note**: yoy may need to disable the antivirus if it detects it as false positive.
2. Follow the instructions and enjoy! 

- For Linux users (or developers):
We will be using Selenium for automating the webpages. The first step is to install it along with the requirements:
```shell
pip install -r requirements.txt
```
then, run

```shell
python run.py
```

## Important Note
The scope of these scripts is NOT to disregard lab safety, which is extremely important for researchers! The purpose is mainly to automate some boring stuff for fun - besides, don't you feel like a chad _cheating the system_?  

On a serious note, most people just find it annoying having to listen to mandatory courses they are not interested in so they skip them manually. The exam can just be passed by failing the first time and completing the answers after knowing the results.  So my question is: does this make sense? Why not just automate this tedious and - for most - time-wasting process?

PS: I'm not responsible for inappropriate use of this software of course ;) Feel free to contact me anytime though if you need help or have some feedback

## Known Issues
- No quiz for the moment, still in the works ;)

## Changelog
- [v1.0.1](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v1.0.1): Bug fixes: fix bug with infinite recursion and popups
- [v1.0.0alpha](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v1.0.0alpha)
  - Updated for the new website
  - Big GUI overhaul!
  - Added option for fast skipping of videos
  - Added login with multiple options
- [v0.2.0](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v0.2.0): new GUI
  - Added GUI with PySimpleGUI
  - In-app help and link
  - Add stoppable thread for selenium driver
  - Source code polishing
  - Misc. fixes
- [v0.1.0](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v0.1.0): first release


## Contribute

Feel free to contribute and open Issue/PRs! 

Here are some ideas of things to be done:

- [x] Create executable for Windows/Mac
- [x] Add GUI
- [x] Automate `chromedriver` installation
- [x] Add other authentication methods if user does not have Easy Auth
- [ ] Add quiz answering
- [ ] Fix final step: although the quiz is answered correctly, the user does not have any prompt about the finished course since the bot crashes
- [ ] Progress bar or better progress print - now each second there is a bit ugly printing
- [ ] Add tests for Windows version
- [ ] Add tests for Mac version
- [ ] Add tests for Linux version
- [ ] ... Any additional feedback!

You may also try reusing some code for automating something else ^^


---

PS: the original scope was to save time, but I took much longer to create this bot rather than just clicking on the screen myself and remembering the answers kkk. Hopefully though, it will save other people's time!

