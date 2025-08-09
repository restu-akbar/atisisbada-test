from selenium.webdriver.common.by import By
from components.button import button
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


# 1. go to index
# 2. click logout
def logout(driver):
    driver.get("https://t3st.atisisbada.id/index.php")
    wait = WebDriverWait(driver, 5)  # timeout

    wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/span[3]/span/img"))
    )
    button(driver, By.XPATH, "/html/body/div[4]/span[3]/span/img")
