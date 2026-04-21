import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
import attach
from dotenv import load_dotenv
import os

DEFAULT_BROWSER_VERSION = "127.0"

def pytest_addoption(parser):
    parser.addoption(
        "--browser_version",
        default=DEFAULT_BROWSER_VERSION
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options
    )
    driver.set_window_size(1920, 1080)

    browser.config.driver = driver
    browser.config.base_url = "https://demoqa.com"
    browser.config.timeout = 5.0

    yield  browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser, selenoid_url)

    browser.quit()

