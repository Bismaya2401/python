from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver (Chrome in this example)
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box
    search_box = driver.find_element("name", "q")

    # Enter "Amazon" and submit the search
    search_box.send_keys("Amazon")
    search_box.send_keys(Keys.RETURN)

    # Wait for a few seconds to see the results
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
