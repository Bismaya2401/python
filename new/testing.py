# testing.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    # Setup: Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Teardown: Quit WebDriver
    driver.quit()


def test_google_search(driver):
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box and enter a query
    search_box = driver.find_element("name", "q")
    search_box.send_keys("Selenium Python")
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    driver.implicitly_wait(5)  # seconds

    # Assert that the title contains the search query
    assert "Selenium Python" in driver.title
