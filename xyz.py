import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("xyz")

@pytest.fixture
def setup():
    # Set up WebDriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_valid_login(setup):
    driver = setup
    driver.get("http://the-internet.herokuapp.com/login")  # Navigate to login page
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "username")))  # Wait for username field

    logger.info("Entering valid username and password.")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Secure Area']")))  # Wait for successful login
    assert "Secure Area" in driver.page_source, "Login failed!"  # Check if login is successful

def test_invalid_login(setup):
    driver = setup
    driver.get("http://the-internet.herokuapp.com/login")  # Navigate to login page
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "username")))  # Wait for username field

    logger.info("Entering invalid username and password.")
    driver.find_element(By.ID, "username").send_keys("invalidUser")
    driver.find_element(By.ID, "password").send_keys("wrongPassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Your username is invalid!')]")))  # Wait for error message
    assert "Your username is invalid!" in driver.page_source, "Error message not displayed!"  # Check for error message
