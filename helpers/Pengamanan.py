from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import unittest
import os
from dotenv import load_dotenv
from components.button import button
from components.form_input import form_input
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from components.checkbox import checkbox
from components.dropdown import Dropdown
from helpers.set_tanggal_buku import set_tgl_buku
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Dilakukan Penganman Pada Nibar P&M Yang diberikan
# di lakukan Setelah Login
def PengamananPM(driver,Nibar):
    time.sleep(1)
    url = os.getenv("url") # https://t3st.atisisbada.id/
    driver.get(f"{url}pages.php?Pg=pengamananPeralatan")
    time.sleep(2)
    filter_pengamanan(driver, Nibar)
    time.sleep(1)
    checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
    time.sleep(1)
    href_button(driver, "javascript:pengamananPeralatan.formBaru()")
    time.sleep(2)
    button(driver, By.ID, "fmnama_pemakai_button")
    time.sleep(1)
    checkbox(
        driver,
        identifier=1,
        by="index",
        table_selector="#PegawaiPilih_cont_daftar > table",
    )
    driver.execute_script("PegawaiPilih.windowSave();")
    
    Dropdown(driver, identifier="fmstatus_pemakai", value="1", by="id")
    time.sleep(1)
    
    form_input(driver, By.ID, "fmno_ktp_pemakai", "12345678")
    form_input(driver, By.ID, "fmalamat_pemakai", "Alamat Testing")
    form_input(driver, By.ID, "fmno_bast", "08/bast/2025")
    form_input(driver, By.ID, "fmtgl_bast","01-05-2025")
        
    Dropdown(driver, identifier="fmdiinput_oleh", value="1", by="id")
    time.sleep(1)
    
    button(driver, By.ID, "fmdiinput_nama_button")
    time.sleep(1)
    checkbox(
        driver,
        identifier=1,
        by="index",
        table_selector="#PegawaiPilih_cont_daftar > table",
    )
    
    time.sleep(1)
    pilih_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
    )
    driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
    time.sleep(3)
    button(driver, By.ID, "btSimpan")
    time.sleep(2)
    
def BatalPengamananPM(driver,Nibar):
    time.sleep(1)
    url = os.getenv("url") # https://t3st.atisisbada.id/
    driver.get(f"{url}pages.php?Pg=pengamananPeralatanTrans")
    time.sleep(2)
    filter_pengamanan(driver, Nibar)
    time.sleep(1)
    checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
    time.sleep(1)
    href_button(driver, "javascript:pengamananPeralatanTrans.Hapus()")
    
    alert = Alert(driver)
    alert_text = alert.text
    print(f"ℹ️ Alert muncul: {alert_text}")
    alert.accept()
    time.sleep(2)
    
    alert = Alert(driver)
    alert_text = alert.text
    print(f"ℹ️ Alert muncul: {alert_text}")
    alert.accept()
    time.sleep(2)
