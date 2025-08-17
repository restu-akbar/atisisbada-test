from asyncio.windows_events import NULL
import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from components.form_input import form_input
from components.button import button
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar
from helpers.logout_helper import logout
from helpers.nama_pemakai_check import nama_pemakai_check
from components.dropdown import Dropdown
from components.alert import alert_handle
from helpers.print_result import print_result
from pages.login_page import LoginPage
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

from selenium.webdriver.common.alert import Alert

import time


class TC_PNPE(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        try:
            # Dismiss any open alerts before logout
            try:
                WebDriverWait(cls.driver, 3).until(EC.alert_is_present())
                Alert(cls.driver).accept()
                print("Closed lingering alert before logout")
            except (TimeoutException, NoAlertPresentException):
                pass  # No alert to close
            logout(cls.driver)
            print(f"✅ Logout berhasil")
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()
            
    def setUp(self):
        load_dotenv()
        self.nibar = os.getenv("nibar")
        self.nama_pemakai = None

    def test_TC_PNPE_001(self):
        print("TC_PNED_001")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=pengembalianPeralatan")
        
        filter_nibar(driver, self.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        href_button(driver, "javascript:pengembalianPeralatan.formEdit()")
        
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"#fmpenyebab_pengembalian > option:nth-child(1)").click()
        button(driver, By.ID, "btSimpan")
        time.sleep(2)
        
        expected_value = "Penyebab Pengembalian belum diisi!"
        alert = Alert(driver)
        alert_text = alert.text
        self.assertEqual(alert_text, expected_value, f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        print_result(alert_text,expected_value,"TC_PNPE_001_01")
        time.sleep(1)
        
        Dropdown(driver, identifier="fmpenyebab_pengembalian", value="2")
        driver.find_element(By.ID,"fmno_bast").clear()
        button(driver, By.ID, "btSimpan")
        time.sleep(2)
        
        expected_value = "Nomor BAST belum diisi!"
        alert = Alert(driver)
        alert_text = alert.text
        self.assertEqual(alert_text, expected_value, f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        print_result(alert_text,expected_value,"TC_PNPE_001_02")
        time.sleep(2)
        
        driver.find_element(By.ID,"fmno_bast").send_keys("newBast")
        driver.find_element(By.ID,"fmtgl_bast").clear()
        button(driver, By.ID, "btSimpan")
        time.sleep(2)
        
        expected_value = "Tanggal BAST belum diisi!"
        alert = Alert(driver)
        print_result(alert.text,expected_value,"TC_PNPE_001_03")
        self.assertEqual(alert_text, expected_value, f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        
        
        
    

       


if __name__ == "__main__":
    unittest.main()
