from selenium.webdriver import Chrome, Firefox, Ie, Edge #, Opera
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.core.os_manager import ChromeType


AVAILABLE_BROWSERS = ['Chrome', 'Chromium', 'Brave', 'Firefox', 'IE', 'Edge']#, 'Opera']


def setup_webdriver(browser):
    if browser.lower() == 'chrome':
        driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    if browser.lower() == 'chromium':
        driver = Chrome(service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    if browser.lower() == 'brave':
        driver = Chrome(service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
    if browser.lower() == 'firefox':
        driver = Firefox(service=FirefoxService(GeckoDriverManager().install()))
    if browser.lower() == 'ie':
        driver = Ie(service=IeService(IEDriverManager().install()))
    if browser.lower() == 'edge':
        driver = Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    # if browser.lower() == 'opera':
    #     driver = Opera(executable_path=OperaDriverManager().install())
    return driver


if __name__ == "__main__":
    setup_webdriver('brave')