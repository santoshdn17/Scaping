import json
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import csv

chrome_driver_path = Service('C:\development\chromedriver.exe')

driver = webdriver.Chrome(service=chrome_driver_path)

product = []

def amazon(t, u, p, d):
    if t == None or u == None or p == None or d == None:
        pass
    else:
        new_product = {
            "product_title" : t,
            "product_image_URL" : u,
            "price_of_the_product" : p,
            "product_details" : d,
        }
        product.append(new_product)
        with open("product.json", "r+") as file:
            json.dump(product, file, indent=4)

error = ["ENTSCHULDIGUNG", "DÉSOLÉ"]

with open("Scraping.csv", "r") as file:
    csv_reader = csv.reader(file)
    for a in csv_reader:
        driver.get(f"https://www.amazon.{a[3]}/dp/{a[2]}")
        try:
            if driver.find_element(By.ID, "h").text in error:
                print(driver.current_url)

        except selenium.common.exceptions.NoSuchElementException:
            try:
                driver.find_element(By.ID, "sp-cc-accept").click()
                title = driver.find_element(By.ID, "productTitle").text
                url = driver.find_element(By.CSS_SELECTOR, "#imgBlkFront").get_attribute("src")
                price = driver.find_element(By.CSS_SELECTOR, "span[class='a-color-base']").text
                details = driver.find_element(By.ID, "detailBullets_feature_div").text
                amazon(title, url, price, details)
            except selenium.common.exceptions.NoSuchElementException:
                pass

driver.quit()
