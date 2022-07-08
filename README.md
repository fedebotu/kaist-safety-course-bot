# KAIST 안전교육 이수 봇

KAIST 안전교육을 자동으로 이수하게 해주는 봇입니다.

> 이 봇은 자동으로 (제법 귀찮은) 연구실 안전교육을 자동으로 이수하게 해주므로, 여러분들은 교육 수료를 위해 몇번이고 비디오를 클릭할 필요가 없습니다. 또한, 퀴즈를 푸는 시간도 버릴 수 없기 때문에 자동적으로 문제도 풀어줍니다 :)


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
4. 주의 : `driver_path`를 [크롬 드라이버](https://chromedriver.chromium.org/downloads)가 설치된 경로에 맞게 수정해야합니다. 환경설정을 확인하세요.
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
봇은 다음과 같은 몇가지 사용자 입력을 필요로 합니다.
- `answer_quiz`: (default=true): 만약 true라면 퀴즈를 자동으로 풉니다. 초기 설정값은 true입니다.
- `driver_path`: (default=/usr/bin/chromedriver) your `chromedriver` path (look at Setup above): 크롬 드라이버의 경로를 입력합니다. (자세한 정보는 위의 내용을 확인하세요)
- `mute_video` (default=true) 만약 true라면 영상이 음소거됩니다. 초기 설정값은 true입니다.
- `target_webpage` (default='https://safety.kaist.ac.kr/main/main.do') 봇이 대상으로 하는 페이지입니다.
- `username` (default='YOUR_USERNAME') KAIST 사용자 이름을 입력합니다.
- `video_id` (default=0) '정기'로 시작하는 영상의 id입니다.

`config.yaml` 파일이 한번 저장되면 위의 사용자 입력을 다시 입력할 필요가 없습니다. 이후에는 몇 개의 웹페이지가 자동으로 팝업되고 작업이 시작됩니다!


## 중요사항

이 문서의 취지는 실험자들에게 아주 중요한 연구실 안전을 무시하려고 함이 아닙니다! 이 봇을 만든 주된 목적은 지루한 작업을 자동화하는 것에 있습니다. - besides, don't you feel like a chad _cheating the system_?  


대부분의 사람들은 관심도 없는 의무 교육을 듣는 것이 지루하다고 느껴 직접 스킵하고는 합니다. 시험은 우선 답을 채운 뒤 채점을 하고, 떨어지더라도 여기서 알아낸 답으로 간단하게 통과할 수 있습니다. 그래서 이게 맞는건가 하는 생각이 들었습니다. 이런 지루하고 시간 낭비인 작업을 자동화하는게 좋을 것 같았습니다.

추신 : 저는 이 소프트웨어를 코스에 대해 부적절하게 사용하는 것에 대해 책임을 지지 않습니다. 도움이 필요하거나 피드백이 있다면 편하게 말씀해주세요.

## Known Issues
- 퀴즈를 통과하면 (60점 이상을 득점해서) 봇이 '다음' 버튼을 찾을 수 없어서 멈추게 됩니다. 이런 경우 우선 퀴즈를 통과했는지 확인하고, `Ctrl+C`를 눌러 스크립트를 멈추게 할 수 있습니다. 페이지를 확인하면서 '완료'와 관련된 키워드를 찾아내면 이런 문제를 해결할 수 있습니다. 
- 지금은 간편 2단계 인증만 지원하기 때문에, 먼저 [설정](https://board.kaist.ac.kr/enboard/iam_notice/11625098246176)에서 인증 설정을 해야합니다.

- 퀴즈를 응시하고 나면 봇은 자동으로 꺼집니다. 교육이 이수가 완료 되었을거에요 ;)


## 변경 내역
- [v0.2.0](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v0.2.0): 신규 GUI
  - PySimpleGUI로 새로운 GUI를 추가했습니다.
  - 인앱 도움말 및 링크를 추가했습니다.
  - 셀레니움(selenium) 드라이버를 위한 stoppable 스레드를 추가했습니다.
  - 코드 정리(polishing)
  - 기타 수정
- [v0.1.0](https://github.com/fedebotu/kaist-safety-course-bot/releases/tag/v0.1.0): 첫번째 릴리즈


## 기여

자유롭게 기여하고 Issue나 PR을 열어보세요!
해야하는 작업들은 다음과 같습니다:

- [x] Window와 Mac 사용자를 위한 실행파일
- [x] GUI 추가
- [ ] `chromedriver` 설치 자동화
- [ ] 교육과정 선택 자동화 (모든 것들이 자동화 될 예정입니다.)
- [ ] 사용자가 간편 인증을 사용할 수 없는 경우 이용할 수 있는 다른 인증 방법
- [ ] 수정 마지막 단계 : 퀴즈가 정상적으로 종료되더라도 봇 또한 자동으로 종료되기 때문에 사용자가 교육이 끝났다는 것을 알 수 없다는 점
- [ ] 상태 표시줄 또는 더 좋은 상태 표현법 - 지금은 매 초마다 조금 못생긴 형태가 프린트됩니다.
- [ ] 윈도우 버전을 위한 테스트 추가
- [ ] 맥 버전을 위한 테스트 추가
- [ ] 리눅스 버전을 위한 테스트 추가
- [ ] ... 그 외의 추가적인 피드백

다른 것을 자동화 하기위해 코드를 Reuse 하실 수 있습니다 ^^

---

추신 : 시간을 절약하자는 것이 본 목적이었으나, 화면을 클릭하고 정답을 기억하느라 봇을 만드는 데에 많은 시간을 들였습니다. 그래도 이 봇이 다른 분들의 시간을 절약할 수 있기를 바랍니다!
