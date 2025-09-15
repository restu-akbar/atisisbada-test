from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def href_button(driver, href_value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    # gunakan CSS: a[href*="..."]
    css = f'a[href*="{href_value}"]'
    try:
        el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        el.click()
    except Exception as e:
        raise Exception(f"Link dengan href berisi '{href_value}' tidak ditemukan/klik: {e}")
