import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from components.form_input import form_input
from components.button import button
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar
from helpers.logout_helper import logout
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
import time
from selenium.webdriver.support import expected_conditions as EC


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
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()

    #         cls.driver.quit()

    def test_TC_PNED_001(self):
        print("TC_PNED_001")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        page = ModulPengamananPage(driver)
        self.assertTrue(
            page.is_loaded(page_name="Pengamanan"), "❌ Modul Pengamanan gagal dimuat"
        )
        time.sleep(1)
        filter_nibar(driver, "167192")
        time.sleep(1)
        checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:pengamananPeralatanTrans.formEdit()")
        time.sleep(1)
        no_ktp_baru = "12345"
        form_input(driver, By.ID, "fmno_ktp_pemakai", no_ktp_baru)
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        time.sleep(1)
        filter_nibar(driver, "167192")
        time.sleep(1)
        cell_value = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[@class='koptable']//tbody/tr[1]/td[11]")
                )
            )
            .text
        )
        assert cell_value == no_ktp_baru, (
            f"[❌] Gagal: nilai no ktp pemakai = {cell_value}, expected = {no_ktp_baru}"
        )
        print(f"[✅] Edit berhasil — Nomor Identitas Pemakai = {cell_value}")


#     def test_TC_PNED_002(self):
#     def test_TC_PNED_003(self):

if __name__ == "__main__":
    unittest.main()
