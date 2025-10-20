import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from components.button import button
from components.form_input import form_input


def filter_pengamanan(driver, text: str, filter="fmFiltNibar"):
    form_input(driver, By.ID, filter, text)
    time.sleep(1)
    button(driver, By.ID, "btTampil")

def filter_gantirugi(driver, text: str, timeout=10):
    form_input(driver,By.ID,"fmid_barang",text)
    time.sleep(1)
    button(driver, By.ID, "btTampil")
    
def filter_formgantirugiPembayaran(driver, text: str, timeout=10):
    form_input(driver, By.ID, "fmidbarang", text)
    time.sleep(1)
    button(driver, By.ID, "btTampil")

def filter_formgantirugi(driver, text: str, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.visibility_of_element_located((By.ID, "nodata")))
    time.sleep(1)
    form_input(driver, By.ID, "nodata", text)
    time.sleep(1)
    button(driver, By.CSS_SELECTOR, "#penatausaha_cont_opt > table:nth-child(3) > tbody > tr > td > div > input[type=button]:nth-child(12)")

def filter_nibar_pembukuan(driver, text, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.visibility_of_element_located((By.ID, "nodata")))
    time.sleep(1)
    form_input(driver, By.ID, "nodata", text)
    time.sleep(1)
    button(driver, By.XPATH, '//input[@type="button" and @value="Tampilkan"]')
