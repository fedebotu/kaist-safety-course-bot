"""
KAIST Safety Course Automatic Viewer

This bot makes viewing the (quite annoying) lab safety videos automatic, so you don't have to click 
many times on the videos that you need to see to complete the course.
Also, considering that as of the time of writing the quiz can not be failed, 
the bot can additionally complete it too :D.

Please read the README.md file for more information on Github:
https://github.com/fedebotu/kaist-safety-course-bot

"""

from kaist.gui.main import main_page


# Run the main GUI app
if __name__ == "__main__":
    main_page()
