from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
# PATH = "/Users/natekim/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.techwithtim.net")
print(driver.title)

search = driver.find_element(By.NAME, "s")
search.clear()
search.send_keys("test")
search.send_keys(Keys.RETURN)

try:
    main = WebDriverWait(driver, 10).until (
        EC.presence_of_element_located((By.ID, "main"))
    )
    
    articles = main.find_elements(By.TAG_NAME, "article")
    for article in articles:
        header = article.find_element(By.CLASS_NAME, "entry-summary")
        print(header.text)
finally:
    driver.quit()