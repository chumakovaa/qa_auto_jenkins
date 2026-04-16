import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    browser.config.base_url = "https://demoqa.com"
    # browser.config.base_url = "https://app.qa.guru"
    browser.config.timeout = 5.0

    # browser.config.driver_name = "firefox"
    # driver_options = webdriver.FirefoxOptions()

    browser.config.driver_name = "chrome"
    driver_options = webdriver.ChromeOptions()

    driver_options.add_argument("--headless")
    browser.config.driver_options = driver_options
    # browser.config.driver.maximize_window()
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    browser.quit()
