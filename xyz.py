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
    options.add_argument("--no-sandbox")  # Required for some environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://the-internet.herokuapp.com/login")
    yield driver
    driver.quit()

def test_valid_login(setup, caplog):
    driver = setup
    logger.info("Entering valid username and password.")
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Secure Area" in driver.page_source, "Login failed: Secure Area not found!"
    logger.info("Login successful.")

def test_invalid_login(setup, caplog):
    driver = setup
    logger.info("Entering invalid username and password.")
    driver.find_element(By.ID, "username").send_keys("invalidUser")
    driver.find_element(By.ID, "password").send_keys("wrongPassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Your username is invalid!" in driver.page_source, "Error message not displayed for invalid login!"
    logger.info("Error message displayed for invalid login.")

    # Capture log output for the report
    for message in caplog.text.splitlines():
        logger.info(message)

