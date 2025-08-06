import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def create_driver():
    load_dotenv()
    url = os.getenv("url")
    brave_path = os.getenv("brave")
    chromedriver_path = os.getenv("driver")
    if not url or not brave_path or not chromedriver_path:
        raise ValueError("ENV tidak ditemukan")

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    print("✅ Driver berhasil dibuat")
    return driver, wait, url
