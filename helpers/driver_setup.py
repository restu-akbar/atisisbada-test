import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def create_driver():
    load_dotenv()
    url = os.getenv("url")
    if not url:
        raise ValueError("URL tidak ditemukan di file .env")

    brave_path = "/usr/bin/brave-browser"
    chromedriver_path = (
        "/home/restu/Downloads/chromedriver138/chromedriver-linux64/chromedriver"
    )

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 15)
        print("✅ Driver berhasil dibuat")
        return driver, wait, url
    except Exception as e:
        print("❌ Gagal membuat driver:", str(e))
        raise
