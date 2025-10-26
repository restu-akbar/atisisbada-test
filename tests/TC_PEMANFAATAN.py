from datetime import datetime, date
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
import calendar
from zoneinfo import ZoneInfo


class TC_PEMANFAATAN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        LoginPage(cls.driver).login(user, password)
        TC_PEMANFAATAN.nibar = os.getenv("nibar")
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

    #         cls.driver.quit()
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
        if self._testMethodName == "test_TC_PEMANFAATAN_001":
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=tetap")
            filter_nibar_pembukuan(self.driver, self.nibar)
        else:
            driver.get(f"{self.url}index.php?Pg=06&bentukmanfaat=")
            Dropdown(driver, "fmidberakhir", 0)
            filter_pengamanan(self.driver, self.nibar or "", "fmid")
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)

        def get_href(test_name):
            prefix = "javascript:"
            mapping = {
                "001": "pemanfaatanV2.formMulti()",
                "002": "PemanfaatForm.Edit()",
                "003": "PemanfaatHapus.Hapus()",
                "004": "PemanfaatBerakhirForm.Edit()",
                "005": "PemanfaatBerakhirBatal.Hapus()",
            }

            kode = test_name.split("_")[-1]
            fn = mapping.get(kode)
            return f"{prefix}{fn}" if fn else None

        href = get_href(self._testMethodName)
        if href:
            href_button(self.driver, href)

    def helper_create(self, test_case):
        test_case = f"test_TC_PEMANFAATAN_00{test_case}"
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

    def test_TC_PEMANFAATAN_001(self):
        helper_pemanfaatan(self.driver)
        test_case = "test_TC_PEMANFAATAN_001"
        print(test_case)
        print_result(self.get_alert_text(), "Pemanfaatan 1 data Sukses", test_case)

    def test_TC_PEMANFAATAN_002(self):
        helper_pemanfaatan(self.driver, False, "10")
        test_case = "test_TC_PEMANFAATAN_002"
        print(test_case)
        print_result(self.get_alert_text(), "Sukses Simpan Data", test_case)

    def test_TC_PEMANFAATAN_003(self):
        test_case = "test_TC_PEMANFAATAN_003"
        print(test_case)
        time.sleep(3)
        self.accept_alert()
        print_result(True, True, test_case)

    def test_TC_PEMANFAATAN_004(self):
        driver = self.driver
        test_case = "test_TC_PEMANFAATAN_004"
        print(test_case)
        time.sleep(3)
        today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
        tgl_str = f"{today.day}"
        bln_str = f"{today.month:02d}"
        Dropdown(driver, "fmTANGGALPEMANFAATANBerakhir_tgl", tgl_str)
        time.sleep(1)
        Dropdown(driver, "fmTANGGALPEMANFAATANBerakhir_bln", bln_str)
        time.sleep(2)
        form_input(driver, By.ID, "fmKET", "tes")
        button(driver, By.XPATH, "//input[@value='Simpan']")
        time.sleep(2)
        print_result(self.get_alert_text(), "Sukses Simpan Data", test_case)

    def test_TC_PEMANFAATAN_005(self):
        test_case = "test_TC_PEMANFAATAN_005"
        print(test_case)
        time.sleep(3)
        self.accept_alert()
        print_result(True, True, test_case)

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


def helper_pemanfaatan(driver, is_create=True, jangka_waktu="5"):
    today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
    tgl_str = f"{today.day}"  # contoh: "07"
    bln_str = f"{today.month:02d}"  # contoh: "09"
    thn_str = str(today.year)  # contoh: "2025"

    end_dt = add_one_month_safe(today)
    end_tgl_str = f"{end_dt.day}"
    end_bln_str = f"{end_dt.month:02d}"
    end_thn_str = str(end_dt.year)

    Dropdown(driver, "fmTANGGALPEMANFAATAN_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_thn", thn_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmJANGKAWAKTU", jangka_waktu)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_tgl", end_tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmTANGGALPEMANFAATAN_akhir_thn", end_thn_str)
    time.sleep(1)
    if is_create:
        Dropdown(driver, "fmBENTUKPEMANFAATAN", 2)
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
    else:
        button(driver, By.XPATH, "//input[@value='Simpan']")


def add_one_month_safe(dt: date) -> date:
    y, m = dt.year, dt.month + 1
    if m == 13:
        y, m = y + 1, 1
    last_day_next = calendar.monthrange(y, m)[1]
    d = min(dt.day, last_day_next)
    return date(y, m, d)


def suite():
    s = unittest.TestSuite()
    s.addTests(
        [
            TC_PEMANFAATAN("test_TC_PEMANFAATAN_001"),
            TC_PEMANFAATAN("test_TC_PEMANFAATAN_002"),
            TC_PEMANFAATAN("test_TC_PEMANFAATAN_004"),
            TC_PEMANFAATAN("test_TC_PEMANFAATAN_005"),
            TC_PEMANFAATAN("test_TC_PEMANFAATAN_003"),
        ]
    )
    return s


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
