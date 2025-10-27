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

from tests.TC_MUTASI.TC_PEMINDAH_TANGANAN import flow_pemindahtanganan_001
from tests.TC_PEMUSNAHAN import flow_pemusnahan_002


# python -m unittest tests.TC_PENGHAPUSAN -k test_TC_PENGHAPUSAN_001
class TC_PENGHAPUSAN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        LoginPage(cls.driver).login(user, password)
        TC_PENGHAPUSAN.nibar = os.getenv("nibar")
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
        name = self._testMethodName

        if name == "test_TC_PENGHAPUSAN_004":
            self.run_pemusnahan_002_precond(self.url, self.nibar)
            flow_pemusnahan_002(driver, True)
            self.__class__._ensure_focus_on_open_window()
            driver.get(f"{self.url}pages.php?Pg=pemusnahan&jns=pelaporan")
            filter_pengamanan(self.driver, self.nibar or "", "fmid_barang")
        elif name == "test_TC_PENGHAPUSAN_005":
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=tetap")
            flow_pemindahtanganan_001(self.driver, self.nibar)
            self.__class__._ensure_focus_on_open_window()
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=pindah")
            filter_nibar_pembukuan(self.driver, self.nibar)

        elif name == "test_TC_PENGHAPUSAN_003":
            driver.get(f"{self.url}index.php?Pg=09&SPg=01&SSPg=03")
            filter_pengamanan(self.driver, self.nibar or "", "id_barang")

        else:
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=tetap")
            filter_nibar_pembukuan(self.driver, self.nibar)

        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)

        href = "javascript:penghapusan_ins.penghapusanbaru(1)"
        if name == "test_TC_PENGHAPUSAN_003":
            href = "javascript:Penghapusan_Hapus()"
        elif name == "test_TC_PENGHAPUSAN_004":
            href = "javascript:penghapusan_ins.penghapusanbaru(3)"

        href_button(driver, href)

    def helper_create(self, test_case, isOther=True):
        test_case = f"test_TC_PENGHAPUSAN_00{test_case}"
        print(test_case)
        driver = self.driver
        time.sleep(2)
        self.accept_alert()
        time.sleep(2)
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception:
            pass
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        if isOther:
            Dropdown(driver, "fmpenyebab", 1)
        time.sleep(1)
        href_button(driver, "javascript:penghapusan_ins.Simpan()")
        time.sleep(1)
        return test_case

    def test_TC_PENGHAPUSAN_001(self):
        test_case = self.helper_create("1")
        self.errmsg_helper(
            test_case,
            f"1. ID {TC_PENGHAPUSAN.nibar} Barang masih dalam pengamanan penggunaan, harus pengembalian!",
        )

    def test_TC_PENGHAPUSAN_002(self):
        test_case = self.helper_create("2")
        alert_text = self.get_alert_text()
        print_result(alert_text, "Penghapusan Selesai !", test_case)

    def test_TC_PENGHAPUSAN_003(self):
        self.accept_alert()
        test_case = "test_TC_PENGHAPUSAN_003"
        time.sleep(3)
        alert_text = self.get_alert_text()
        print_result(alert_text, "Data sukses di batalkan", test_case)

    def test_TC_PENGHAPUSAN_004(self):
        test_case = self.helper_create("4", False)
        alert_text = self.get_alert_text()
        print_result(alert_text, "Penghapusan Selesai !", test_case)

    def test_TC_PENGHAPUSAN_005(self):
        test_case = self.helper_create("5")
        alert_text = self.get_alert_text()
        print_result(alert_text, "Penghapusan Selesai !", test_case)

    def run_pemusnahan_002_precond(self, url, nibar):
        self.driver.get(f"{url}index.php?Pg=05&SPg=03&jns=tetap")
        filter_nibar_pembukuan(self.driver, nibar)
        time.sleep(1)
        checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(self.driver, "javascript:pemusnahan_ins.pemusnahanbaru()")

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
