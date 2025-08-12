import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar
from helpers.logout_helper import logout
from helpers.nama_pemakai_check import nama_pemakai_check
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TC_PNBT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_PNBT.nibar = os.getenv("nibar")
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

    def setUp(self):
        driver = self.driver
        if self._testMethodName in ["test_TC_PNBT_001", "test_TC_PNBT_003"]:
            driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
            time.sleep(1)
            filter_nibar(driver, self.nibar)
            time.sleep(1)
            checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
            time.sleep(1)
            href_button(driver, "javascript:pengamananPeralatanTrans.Hapus()")
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            except TimeoutException:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()

            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            except TimeoutException:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            self.alert_text = alert.text
            alert.accept()

    def test_TC_PNBT_001(self):
        print("TC_PNBT_001")
        print_result(self.alert_text, "Sukses Hapus Data", "TC_PNBT_001")

    def test_TC_PNBT_002(self):
        print("TC_PNBT_002")
        actual = nama_pemakai_check(self).strip()
        expected = ""

        if actual != expected:
            print_result(actual, expected, test_name="TC_PNBT_002")
            raise AssertionError(
                "[❌] Gagal: nama pemakai masih ada, pemakaian gagal dihapus"
            )
        else:
            print_result(actual, expected, test_name="TC_PNBT_002")

    def test_TC_PNBT_003(self):
        print("TC_PNBT_003")
        print_result(self.alert_text, "Sukses Hapus Data", "TC_PNBT_001")


if __name__ == "__main__":
    unittest.main()
