# KAIST 안전교육 이수 봇

KAIST 안전교육을 자동으로 이수하게 해주는 봇입니다.

> 이 봇은 자동으로 (제법 귀찮은) 연구실 안전교육을 자동으로 이수하게 해주므로, 여러분들은 교육 수료를 위해 몇번이고 비디오를 클릭할 필요가 없습니다. 또한, 퀴즈를 푸는 시간도 버릴 수 없기 때문에 자동적으로 문제도 풀어줍니다 :).


## 앱 스크린샷

<p align="center">
  <img src="assets/app-screenshot.png" width = 40% alt="Image">
</p>

## 사용법
우선, [KAIST 안전교육 사이트](https://safety.kaist.ac.kr/main/main.do)에서 이수하고자 하는 교육을 선택합니다. 각 운영체제별 사용법은 다음과 같습니다 :

- 윈도우/맥 사용자 : 
1. 크롬을 사용하기 위해 [크롬 드라이버](https://chromedriver.chromium.org/downloads)를 설치하고 경로에 맞게 옮겨주세요. (구글에서 운영체제에 맞는 설치 도움말을 찾아보세요)
2. [릴리즈 페이지](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v0.2.0)에서 운영체제에 맞는 파일을 다운로드하고 실행하세요.
3. exe파일을 실행합니다.
4. 주의 : `driver_path`를 [크롬 드라이버](https://chromedriver.chromium.org/downloads)가 설치된 경로에 맞게 수정해야합니다. ([환경설정]을 확인하세요(#configuration-settings))
5. 끝났습니다! 

- 리눅스 사용자 (혹은 개발자):
웹페이지를 자동으로 처리하기 위해서는 Selenium을 이용해야하므로, 다음과 같이 설치를 시작합니다.
```shell
pip install -r requirements.txt
```
그리고 다음과 같이 실행합니다.

```shell
python kaist-safety-course-bot.py
```

## 환경설정
The bot will ask for a few configuration inputs:
봇은 다음과 같은 몇가지 사용자 입력을 필요로 합니다.
- `answer_quiz`: (default=true): 만약 true라면 퀴즈를 자동으로 풉니다. 초기 설정값은 true입니다.
- `driver_path`: (default=/usr/bin/chromedriver) your `chromedriver` path (look at Setup above): 크롬 드라이버의 경로를 입력합니다. (자세한 정보는 위의 내용을 확인하세요)
- `mute_video` (default=true) mute video : 만약 true라면 영상이 음소거됩니다. 초기 설정값은 true입니다.
- `target_webpage` (default='https://safety.kaist.ac.kr/main/main.do') 봇이 대상으로 하는 페이지입니다.
- `username` (default='YOUR_USERNAME') KAIST 사용자 이름을 입력합니다.
- `video_id` (default=0) '정기'로 시작하는 영상의 id입니다.

A `config.yaml` file will be saved so that you don't need to re-add these again.
`config.yaml` 파일이 한번 저장되면 위의 사용자 입력을 다시 입력할 필요가 없습니다.
You should then see some webpages automatically popping up and doing stuff!


## Important Note
The scope of these scripts is NOT to disregard lab safety, which is extremely important for researchers! The purpose is mainly to automate some boring stuff for fun - besides, don't you feel like a chad _cheating the system_?  

On a serious note, most people just find it annoying having to listen to mandatory courses they are not interested in so they skip them manually. The exam can just be passed by failing the first time and completing the answers after knowing the results.  So my question is: does this make sense? Why not just automate this tedious and - for most - time-wasting process?

PS: I'm not responsible for inappropriate use of this software of course ;) Feel free to contact me anytime though if you need help or have some feedback

## Known Issues
- When the quiz is passed (>=60 points scored) the bot gets stuck since it cannot find the "NEXT" button. In this case, check if the quiz has been passed and you can stop the script with `Ctrl+C`. This could be fixed by checking the page source for keywords related to the completion.
- Only Easy Authentication works for now (간편 2단계 인증), so you need to set it up first [Setup instructions](https://board.kaist.ac.kr/enboard/iam_notice/11625098246176)
- After answering the quiz, the bot crashes: if it does though good news, you should have completed the lesson ;)

## Changelog
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
- [ ] Automate `chromedriver` installation
- [ ] Automatic course selection (everything would be automatic this way)
- [ ] Add other authentication methods if user does not have Easy Auth
- [ ] Fix final step: although the quiz is answered correctly, the user does not have any prompt about the finished course since the bot crashes
- [ ] Progress bar or better progress print - now each second there is a bit ugly printing
- [ ] Add tests for Windows version
- [ ] Add tests for Mac version
- [ ] Add tests for Linux version
- [ ] ... Any additional feedback!

You may also try reusing some code for automating something else ^^


---

PS: the original scope was to save time, but I took much longer to create this bot rather than just clicking on the screen myself and remembering the answers kkk. Hopefully though, it will save other people's time!

