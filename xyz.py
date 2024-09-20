import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def setup():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for faster execution
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://the-internet.herokuapp.com/login")
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password, expected", [
    ("tomsmith", "SuperSecretPassword!", "Secure Area"),
    ("invalidUser", "wrongPassword", "Your username is invalid!")
])
def test_login(setup, username, password, expected, caplog):
    driver = setup
    logger.info(f"Entering username: {username} and password: {password}.")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    if expected == "Secure Area":
        assert "Secure Area" in driver.page_source, "Login failed!"
        logger.info("Login successful.")
    else:
        assert "Your username is invalid!" in driver.page_source, "Error message not displayed!"
        logger.info("Error message displayed for invalid login.")

    # Capture log output for the report
    for message in caplog.text.splitlines():
        logger.info(message)
