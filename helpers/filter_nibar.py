import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from components.button import button
from components.form_input import form_input


def filter_nibar(driver, text, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.visibility_of_element_located((By.ID, "fmFiltNibar")))
    time.sleep(1)
    form_input(driver, By.ID, "fmFiltNibar", text)
    time.sleep(1)
    button(driver, By.ID, "btTampil")
