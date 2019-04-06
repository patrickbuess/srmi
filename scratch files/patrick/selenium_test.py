from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

# OPEN FIREFOX TO NAVIGATE WEBSITE
driver = webdriver.Firefox()
driver.get("https://www.comparis.ch/immobilien/result")
assert "Immobilien" in driver.title

# TYPE IN POSTAL CODE AND HIT ENTER
searchField = driver.find_element_by_id("SearchParams_LocationSearchString")
searchField.send_keys("8000")
searchField.send_keys(Keys.ENTER)

# WAIT 5 SECONDS AND GET CURRENT URL
time.sleep(5)
initialUrl = driver.current_url

# FIND OUT HOW MANY PAGES THERE ARE
nrOfPages = int(driver.find_element_by_css_selector("ul.pagination li:nth-last-child(2) a").get_attribute("innerHTML"))
print("Nr of Pages = "+str(nrOfPages))

# PRESS PAGINATION NEXT BUTTON (NECESSARY TO GET THE SECOND PAGE URL, WHICH CAN BE USED TO GENERATE ALL REMAINING URLS)
nextButton = driver.find_element_by_css_selector('.pagination-next a')
nextButton.click()

# GET URL OF SECOND PAGE
time.sleep(5)
secondUrl = driver.current_url

# CREATE ALL REMAINING URLS
allUrls = [initialUrl, secondUrl]
plainUrl = re.sub('&page=1', '', secondUrl)

for i in range(2,nrOfPages):
    allUrls.append(plainUrl+"&page="+str(i))

print(allUrls)
print("First URL: "+initialUrl)
print("Second URL: "+secondUrl)
print("Nr of Pages = "+str(nrOfPages))
