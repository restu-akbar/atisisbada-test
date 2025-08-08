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

    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    chromedriver_path = (
        "chromedriver.exe"
    )

    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path))
        driver.maximize_window()
        wait = WebDriverWait(driver, 15)
        print("✅ Driver berhasil dibuat")
        return driver, wait, url
    except Exception as e:
        print("❌ Gagal membuat driver:", str(e))
        raise
