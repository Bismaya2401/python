from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestLogin:
    def setup_method(self):
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")  # Required for some environments
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        self.driver = webdriver.Chrome(service=ChromeService(), options=options)  # Initialize the WebDriver
        self.driver.get("http://the-internet.herokuapp.com/login")  # Load the login page

    def teardown_method(self):
        if self.driver:
            self.driver.quit()  # Close the browser after each test

    def test_valid_login(self):
        logger.info("Entering valid username and password.")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the "Secure Area" header to be present after login
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )
            assert "Secure Area" in self.driver.page_source, "Login failed! Secure Area not found."
            logger.info("Login succeeded.")
        except Exception as e:
            logger.error(f"Error during valid login test: {e}")

    def test_invalid_login(self):
        logger.info("Entering invalid username and password.")
        self.driver.find_element(By.ID, "username").send_keys("invalid_user")
        self.driver.find_element(By.ID, "password").send_keys("invalid_password")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the error message to be displayed
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#flash"))
            )
            assert "Your username is invalid!" in self.driver.page_source, "Error message not displayed!"
            logger.info("Invalid login test passed.")
        except Exception as e:
            logger.error(f"Error during invalid login test: {e}")

# Run the tests
if __name__ == "__main__":
    test = TestLogin()
    test.setup_method()
    try:
        test.test_valid_login()
        test.test_invalid_login()
    finally:
        test.teardown_method()
