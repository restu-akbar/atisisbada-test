import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from components.dropdown import Dropdown
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar_pembukuan, filter_pengamanan
from helpers.logout_helper import logout
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time


class TC_MUTASI_SKPD_DARI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        LoginPage(cls.driver).login(user, password)
        TC_MUTASI_SKPD_DARI.nibar = os.getenv("nibar")
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

    def _return_to_main_and_close_extras(self):
        try:
            windows = self.driver.window_handles
            if (
                hasattr(self.__class__, "main_window")
                and self.__class__.main_window in windows
            ):
                keep = self.__class__.main_window
            else:
                keep = windows[0]
                self.__class__.main_window = keep

            for w in list(windows):
                if w != keep:
                    self.driver.switch_to.window(w)
                    try:
                        self.driver.close()
                    except Exception:
                        pass
            self.driver.switch_to.window(keep)
        except Exception:
            pass

    def setUp(self):
        self.__class__._ensure_focus_on_open_window()

        driver = self.driver
        if self._testMethodName == "test_TC_MUTASI_SKPD_DARI_001":
            driver.get(f"{self.url}index.php?Pg=05&SPg=03&jns=tetap")
            filter_nibar_pembukuan(self.driver, self.nibar)
        else:
            driver.get(
                f"{self.url}pages.php?dPg=mutasi&Pg=mutasidari&SSPg=03&menu=pelaporan"
            )
            filter_pengamanan(self.driver, self.nibar or "", "id_barang")

        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)

    def test_TC_MUTASI_SKPD_DARI_001(self):
        driver = self.driver
        href_button(driver, "javascript:MutasiBaru_ins.mutasibaru()")
        time.sleep(1)
        self.accept_alert()
        time.sleep(1)

        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception:
            pass

        time.sleep(1)
        Dropdown(driver, identifier="fmSKPDUrusan", value=1)
        time.sleep(1)
        Dropdown(driver, identifier="fmSKPDBidang2", value=1)
        time.sleep(1)
        Dropdown(driver, identifier="fmSKPDskpd2", value=1)
        time.sleep(1)
        Dropdown(driver, identifier="fmSKPDUnit2", value=1)
        time.sleep(1)
        Dropdown(driver, identifier="fmSKPDSubUnit2", value=1)
        time.sleep(1)
        Dropdown(driver, identifier="no_bast", value=2)
        time.sleep(1)
        href_button(driver, "javascript:MutasiBaru_ins.Simpan(0)")
        time.sleep(1)

        alert_text = self.get_alert_text()
        print_result(
            alert_text, "Mutasi Selesai !", test_name="TC_MUTASI_SKPD_DARI_001"
        )

        self._return_to_main_and_close_extras()

    def test_TC_MUTASI_SKPD_DARI_002(self):
        driver = self.driver
        time.sleep(1)
        href_button(driver, "javascript:Batal_Mutasi()")
        time.sleep(1)
        self.accept_alert()
        alert_text = self.get_alert_text()
        print_result(
            alert_text,
            "Sukses dibatalkan",
            test_name="TC_MUTASI_SKPD_DARI_002",
        )

    def accept_alert(self):
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        except Exception:
            pass

    def get_alert_text(self, timeout=5, auto_accept=True):
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
