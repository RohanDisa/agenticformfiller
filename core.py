# utils/scraper.py
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def extract_form_elements(driver):
    input_elements = driver.find_elements(By.XPATH, '//input')
    select_elements = driver.find_elements(By.XPATH, '//form//select')
    radio_elements = driver.find_elements(By.XPATH, '//input[@type="radio"]')
    checkbox_elements = driver.find_elements(By.XPATH, '//form//input[@type="checkbox"]')
    button_elements = driver.find_elements(By.XPATH, '//form//button')

    return {
        "inputs": input_elements,
        "selects": select_elements,
        "radios": radio_elements,
        "checkboxes": checkbox_elements,
        "buttons": button_elements,
    }
