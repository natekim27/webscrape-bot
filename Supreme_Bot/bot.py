import requests
import json

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from sympy import Product

from config import PaymentDetails, UserDetails, ProductDetails


headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
           'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) " 
                    "Version/13.0.3 Mobile/15E148 Safari/604.1"}

prefs = {'disk-cache-size': 4096}

options = Options()
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("useAutomationExtension", False)

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=PATH)
wait = WebDriverWait(driver, 10)


def find_item(name):
    url = "https://www.supremenewyork.com/mobile_stock.json"
    html = requests.get(url)
    output = json.loads(html.text)
    
    for category in output["products_and_categories"]:
        print(category)
        for item in output["products_and_categories"][category]:
            if name in item['name']:
                print(item["name"])
                print(item["id"])
                return item["id"]
    

def get_color(item_id, color, size):
    url = f"https://www.supremenewyork.com/shop/{item_id}.json"
    html = requests.get(url)
    output = json.loads(html.text)
    
    for product_color in output["styles"]:
        if color in product_color["name"]:
            for product_size in product_color["sizes"]:
                if size in product_size["name"]:
                    return product_color["id"]


def get_product(item_id, color_id, size):
    url = "https://www.supremenewyork.com/mobile/#products/" + str(item_id) + "/" + str(color_id)
    driver.get(url)
    
    wait.until(EC.presence_of_element_located((By.ID, "size-options")))
    
    options = Select(driver.find_element(By.ID,"size-options"))
    options.select_by_visible_text(size)
    
    driver.find_element(By.XPATH, '//*[@id="cart-update"]/span').click()
    
    
def checkout():
    url = "https://www.supremenewyork.com/mobile/#checkout"
    driver.get(url)
    
    wait.until(EC.presence_of_element_located((By.ID, "order_billing_name")))
    
    driver.execute_script(
        f"document.getElementById('order_billing_name').value = '{UserDetails.NAME}'"
        f"document.getElementById('order_email').value = '{UserDetails.EMAIL}'"
        f"document.getElementById('order_tel').value = '{UserDetails.TELE}'"
        f"document.getElementById('order_billing_address').value = '{UserDetails.ADDRESS1}'"
        f"document.getElementById('order[billing_address_2]').value = '{UserDetails.ADDRESS2}'"
        f"document.getElementById('order_billing_zip').value = '{UserDetails.ZIP}'"
        f"document.getElementById('order_billing_city').value = '{UserDetails.CITY}'"
        f"document.getElementById('credit_card_number').value = '{PaymentDetails.CARD_NUMBER}'"
        f"document.getElementById('credit_card_verification_value').value = '{PaymentDetails.CVV}'"
    )
    
    state = Select(driver.find_element(By.ID, "order_billing_state"))
    state.select_by_visible_text(UserDetails.STATE)
    
    card_month = Select(driver.find_element(By.ID, "credit_card_month"))
    card_month.select_by_visible_text(str(PaymentDetails.MONTH))
    
    card_year = Select(driver.find_element(By.ID, "credit_card_year"))
    card_year.select_by_visible_text(str(PaymentDetails.YEAR))
    
    driver.find_element(By.ID, "order_terms").click()
    
    #driver.find_element(By.ID, "submit_button").click()
    

if __name__ == "__main__":
    print("upating rpr")
    
    item_id = find_item(ProductDetails.KEYWORDS)
    color_id = get_color(item_id, ProductDetails.COLOR, ProductDetails.SIZE)
    get_product(item_id, color_id, ProductDetails.SIZE)
    checkout()