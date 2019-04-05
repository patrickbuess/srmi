from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("https://www.comparis.ch/immobilien/result")
assert "Immobilien" in driver.title

searchField = driver.find_element_by_id("SearchParams_LocationSearchString")
searchField.send_keys("8000")
searchField.send_keys(Keys.ENTER)

time.sleep(5)
print(driver.current_url)
