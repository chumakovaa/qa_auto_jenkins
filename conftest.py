import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import browser
import attach

@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "127.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
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
    attach.add_video(browser)

    browser.quit()