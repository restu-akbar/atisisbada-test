import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from components.button import button
from components.dropdown import Dropdown
from components.checkbox import checkbox
from components.form_input import form_input
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar_pembukuan, filter_pengamanan
from helpers.logout_helper import logout
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time

# python -m unittest tests.TC_PEMUSNAHAN -k test_TC_PEMUSNAHAN_001
class TC_PEMUSNAHAN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        LoginPage(cls.driver).login(user, password)
        TC_PEMUSNAHAN.nibar = os.getenv("nibar")
        cls.main_window = cls.driver.current_window_handle
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        try:
            cls._ensure_focus_on_open_window()
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            try:
                cls.driver.quit()
            except Exception:
                pass

    @classmethod
    def _ensure_focus_on_open_window(cls):
        try:
            windows = cls.driver.window_handles
            if not windows:
                cls.driver.switch_to.new_window("tab")
                windows = cls.driver.window_handles

            if hasattr(cls, "main_window") and cls.main_window in windows:
                cls.driver.switch_to.window(cls.main_window)
            else:
                cls.main_window = windows[0]
                cls.driver.switch_to.window(cls.main_window)
        except Exception:
            try:
                cls.driver.switch_to.new_window("tab")
                cls.main_window = cls.driver.window_handles[0]
                cls.driver.switch_to.window(cls.main_window)
            except Exception:
                pass

    def setUp(self):
        self.__class__._ensure_focus_on_open_window()

        driver = self.driver
        if self._testMethodName != "test_TC_PEMUSNAHAN_003":
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=tetap")
            filter_nibar_pembukuan(self.driver, self.nibar)
        else:
            driver.get(f"{self.url}pages.php?Pg=pemusnahan")
            filter_pengamanan(self.driver, self.nibar or "", "fmid_barang")
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href = "javascript:pemusnahan_ins.pemusnahanbaru()"
        if self._testMethodName == "test_TC_PEMUSNAHAN_003":
            href = "javascript:pemusnahan.Hapus()"
        href_button(driver, href)

    def helper_create(self, test_case):
        test_case = f"test_TC_PEMUSNAHAN_00{test_case}"
        print(test_case)
        driver = self.driver
        self.accept_alert()
        time.sleep(1)
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception:
            pass
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        form_input(driver, By.ID, "cr_pemusnahan", "tes")
        time.sleep(1)
        href_button(driver, "javascript:pemusnahan_ins.Simpan3()")
        time.sleep(1)
        return test_case

    def test_TC_PEMUSNAHAN_001(self):
        test_case = self.helper_create("1")
        self.errmsg_helper(
            test_case,
            f"1. ID {TC_PEMUSNAHAN.nibar} NIBAR {TC_PEMUSNAHAN.nibar} masih dalam pengamanan penggunaan, harus pengembalian!",
        )

    def test_TC_PEMUSNAHAN_002(self):
        test_case = self.helper_create("2")
        alert_text = self.get_alert_text()
        print_result(alert_text, "Pemusnahan Selesai !", test_case)

    def test_TC_PEMUSNAHAN_003(self):
        self.accept_alert()
        test_case = "test_TC_PEMUSNAHAN_003"
        alert_text = self.get_alert_text()
        print_result(alert_text, "Sukses Hapus Data", test_case)

    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        except Exception:
            pass

    def errmsg_helper(self, testCase, expected, errMsgId="errmsg", alert=True):
        if alert:
            alert = self.wait.until(EC.alert_is_present())
            if alert:
                alert.accept()
        time.sleep(3)
        try:
            textarea = self.wait.until(
                EC.presence_of_element_located((By.ID, errMsgId))
            )
            value = textarea.get_attribute("value") or ""
            actual = value.strip()

            print_result(actual, expected, testCase)
        except TimeoutException:
            self.fail("[❌] Textarea dengan id 'errmsg' tidak ditemukan")

    def get_alert_text(self, timeout=5, auto_accept=True):
        time.sleep(3)
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            if auto_accept:
                alert.accept()
            return text
        except (TimeoutException, NoAlertPresentException):
            return None
        except Exception:
            return None
