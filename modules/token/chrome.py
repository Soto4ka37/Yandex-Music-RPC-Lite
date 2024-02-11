import json
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager


def is_active(driver):
    try:
        driver.execute(Command.GET_ALL_COOKIES)
        return True
    except Exception:
        return False


def get_token() -> str:
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              executable_path=ChromeDriverManager().install())
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d")

    token = None

    while token == None and is_active(driver):
        sleep(1)
        try:
            logs_raw = driver.get_log("performance")
        except:
            pass

        for lr in logs_raw:
            log = json.loads(lr["message"])["message"]
            url_fragment = log.get('params', {}).get('frame', {}).get('urlFragment')

            if url_fragment:
                token = url_fragment.split('&')[0].split('=')[1]

    try:
        driver.close()
    except:
        pass

    return token