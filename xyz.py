import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def setup_method(request):
    driver = webdriver.Chrome()  # Initialize the WebDriver
    driver.get("http://the-internet.herokuapp.com/login")  # Load the login page
    request.cls.driver = driver
    yield
    driver.quit()  # Close the browser after tests

@pytest.mark.usefixtures("setup_method")
class TestLogin:
    def test_valid_login(self):
        logger.info("Entering valid username and password.")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the "Secure Area" header to be present after login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        assert "Secure Area" in self.driver.page_source, "Login failed! Secure Area not found."

    def test_invalid_login(self):
        logger.info("Entering invalid username and password.")
        self.driver.find_element(By.ID, "username").send_keys("invalid_user")
        self.driver.find_element(By.ID, "password").send_keys("invalid_password")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the error message to be displayed
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#flash"))
        )
        assert "Your username is invalid!" in self.driver.page_source, "Error message not displayed!"

# Run the tests using pytest
if __name__ == "__main__":
    pytest.main()
