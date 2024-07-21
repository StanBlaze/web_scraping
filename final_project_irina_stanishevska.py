from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import requests
import json
import csv
import os

# Функція для отримання кукі у вигляді дикта
def get_cookies_as_dict(driver):
    cookies = driver.get_cookies()
    return {cookie['name']: cookie['value'] for cookie in cookies}

# Функція для збереження даних про ціни у файл CSV
def save_price_data_to_csv(price_data, age, period):
    filename = 'price_data.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['ID', 'priceTotal', 'pricePolicy', 'priceIPT', 'priceNet', 'Age', 'Period'])
        for item_id, item_data in price_data.items():
            writer.writerow([item_id, item_data['priceTotal'], item_data['pricePolicy'], item_data['priceIPT'], item_data['priceNet'], age, period])
    print(f"Data saved to {filename}")

# Основна функція для виконання скрипту
def run_script(age, period):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://admin:admin37@test.globelink.eu/wizard#/step1.html?country_id=4")
        print("Page loaded")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Login successful")

        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()
            print("Alert accepted")
        except Exception as e:
            print(f"No alert found: {e}")

        time.sleep(2)

        single_trip_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'Single Trip')]"))
        )
        single_trip_button.click()
        print("Clicked on 'Single Trip' button")

        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element_attribute((By.XPATH, "//button[contains(@class, 'Single Trip')]"), "aria-pressed", "true")
        )
        print("aria-pressed is now 'true' for 'Single Trip' button")

        europe_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'Europe') and contains(., 'inc. Egypt & Morocco')]"))
        )
        europe_button.click()
        print("Clicked on 'Europe inc. Egypt & Morocco' button")

        age_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "first__step__age__input"))
        )
        age_input.clear()
        age_input.send_keys(str(age))
        print(f"Entered age {age}")

        body_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        body_element.click()
        print("Clicked on body element to proceed")

        calendar_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@class, 'date__input__icon__svg')]"))
        )
        driver.execute_script("arguments[0].click();", calendar_icon)
        print("Clicked on calendar icon")

      
