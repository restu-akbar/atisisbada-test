import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from components.button import button
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
import time


class TestPengamanan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        print("✅ Login berhasil")
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        #         try:
        #             logout(cls.driver)
        #         except Exception as e:
        #             print(f"⚠️ Logout gagal: {e}")
        #         finally:
        #             cls.driver.quit()
        cls.driver.quit()

    def test_TC_PNED_001(self):
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        page = ModulPengamananPage(driver)
        self.assertTrue(
            page.is_loaded(page_name="Pengamanan"), "❌ Modul Pengamanan gagal dimuat"
        )
        time.sleep(2)
        checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:pengamananPeralatanTrans.formEdit()")
        time.sleep(2)
        button(driver, By.ID, "btSimpan")


#     def test_TC_PNED_002(self):
#     def test_TC_PNED_003(self):

if __name__ == "__main__":
    unittest.main()
