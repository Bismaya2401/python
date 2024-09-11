from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (Chrome in this example)
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")

    # Use WebDriverWait to wait for the search box to be present
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

    # Enter "Amazon" and submit the search
    search_box.send_keys("Amazon")
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to be visible
    wait.until(EC.presence_of_element_located((By.ID, "search")))

finally:
    # Close the browser
    driver.quit()
