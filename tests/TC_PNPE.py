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
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
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
            logout(cls.driver)
         
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
        Dropdown(driver, identifier="fmpenyebab_pengembalian", value="4")
        time.sleep(2)
        
        #Example:CSS Selector
        #fmpenyebab_pengembalian > option:nth-child(2)
        #fmpenyebab_pengembalian > option:nth-child(1)
        #fmstatus_pemakai > option:nth-child(6)
        
        
    

       


if __name__ == "__main__":
    unittest.main()
