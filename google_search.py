import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup():
    # Use webdriver-manager to automatically handle the driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://the-internet.herokuapp.com/login")
    yield driver
    driver.quit()

def test_valid_login(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    assert "Secure Area" in driver.page_source, "Login failed!"

def test_invalid_login(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("invalidUser")
    driver.find_element(By.ID, "password").send_keys("wrongPassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    assert "Your username is invalid!" in driver.page_source, "Error message not displayed!"
