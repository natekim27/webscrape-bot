from argparse import Action
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
# PATH = "/Users/natekim/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://orteil.dashnet.org/cookieclicker/")

try:
    language = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, "langSelect-EN"))
    )
    language.click()
except:
    driver.quit()

driver.implicitly_wait(5)

cookie = driver.find_element(By.ID, "bigCookie")
cookie_count = driver.find_element(By.ID, "cookies")
items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1,-1,-1)]

actions = ActionChains(driver)

for i in range(1000):
    actions.click(cookie)
    actions.perform()
    
    count = int(cookie_count.text.split(" ")[0])
    
    for item in items:
        value = int(item.text)
        if value <= count:
            upgrade_actions = ActionChains(driver)
            upgrade_actions.move_to_element(item)
            upgrade_actions.click()
            upgrade_actions.perform()