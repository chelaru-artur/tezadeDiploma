from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib
import cv2
import numpy as np
import base64
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def get_image_text(image):
    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    text = pytesseract.image_to_string(img)
    return text
driver = webdriver.Chrome()
SEARCH_FILTERS_SELECTOR = "[data-marker=search-filters]"
driver.get("https://www.avito.ru/rossiya/avtomobili")
try:
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_FILTERS_SELECTOR)))
    except:
        print("entered")
        driver.close()

    searchFilters = driver.find_element(By.CSS_SELECTOR, SEARCH_FILTERS_SELECTOR)
    priceFrom = driver.find_element(By.CSS_SELECTOR, "[data-marker='price/from']")
    priceFrom.send_keys(1000000)
    submitBtn = driver.find_element(By.CSS_SELECTOR, "[data-marker='search-filters/submit-button']")
    driver.implicitly_wait(100)
    submitBtn.click()
    items = driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
    for i in items[:10]:
        i.click()
    availableTabs = driver.window_handles
    print("window handles %d", len(availableTabs))
    for tab in availableTabs[1:]:
        driver.switch_to.window(tab)
        btn = driver.find_element(By.CSS_SELECTOR, "[data-marker='item-phone-button/card']")
        btn.click()
        print(driver.find_element(By.CSS_SELECTOR, "[data-marker='seller-info/name']").text)
        img = btn.find_element(By.TAG_NAME, 'img').get_attribute('src')
        img_text = get_image_text(img.replace('data:image/png;base64,', ''))
        print (img_text)
        driver.implicitly_wait(1000)

    time.sleep(30)
    # print(elem.text)
    # assert "Python" in driver.title
    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
finally:
    driver.close()


