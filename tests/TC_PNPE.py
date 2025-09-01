from datetime import datetime
import unittest
import os
import re
from dotenv import load_dotenv
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.PM.save_get_alert import save_get_alert
from components.dropdown import Dropdown
from components.form_input import form_input
from components.button import button
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from helpers.nama_pemakai_check import nama_pemakai_check
from helpers.print_result import print_result
from helpers.set_tanggal_buku import set_tgl_buku
from helpers.clear_readonly_input import clear_readonly_input
from pages.login_page import LoginPage
import time

from tests.TC_PNBK import TC_PNBK


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
        driver = cls.driver
        TC_PNPE.nibar = os.getenv("nibar")  # Set nibar on TC_PNPE
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengembalianPeralatan")
        time.sleep(1)
        cls.shared = {}
        cls.tc_pnbk = TC_PNBK()
        cls.tc_pnbk.driver = cls.driver

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
                    print(f"⚠️ Logout gagal: {e}")
        #         finally:
        #             cls.driver.quit()
        #
        cls.driver.quit()

    def setUp(self):
        if self._testMethodName in ["test_TC_PNPE_001","test_TC_PNPE_002"]:
            filter_pengamanan(self.driver, TC_PNPE.nibar or "")
            time.sleep(1)
            checkbox(
                self.driver, identifier=-1, by="index", table_selector="table.koptable"
            )
            time.sleep(1)
            href_button(self.driver, "javascript:pengembalianPeralatan.formEdit()")
            time.sleep(2)

    def _dismiss_if_alert(self, driver):
        try:
            driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        except Exception:
            pass
        
    def test_TC_PNPE_001(self):
        print("test_TC_PNPE_001")
        driver = self.driver

        driver.find_element(By.CSS_SELECTOR, "#fmpenyebab_pengembalian > option:nth-child(3)").click()
        driver.find_element(By.ID, "fmno_bast").clear()
        driver.find_element(By.ID, "fmtgl_bast").clear()

        penyebab = "Purnatugas /Pensiun"
        no_bast = f"New/NO/BAST/{datetime.now()}"
        tgl_bast = datetime.now().strftime("%d-%m-%Y")
        
        driver.find_element(By.ID, "fmtgl_bast").send_keys(tgl_bast)
        driver.find_element(By.ID, "fmno_bast").send_keys(no_bast)
        dt = datetime.now()
        changed_dt = dt.replace(month=9, day=10).strftime("%d-%m-%Y")
        set_tgl_buku(self.driver, changed_dt)
        
        time.sleep(3)
        button(driver, By.ID, "btSimpan")
        
        def clean_status(s: str | None) -> str:
            if not s:
                return ""
            s = s.replace("\xa0", " ").strip()
            s = re.sub(r"^\s*(?:lainnya:\s*)?", "", s, flags=re.I)
            s = re.sub(r"^\s*\d+\.\s*", "", s)
            return s.strip()
        
        def check_or_fail(field_name: str, expected, actual):
            expected_str = clean_status(expected)
            actual_str = clean_status(actual)
            if expected_str != actual_str:
                print_result(
                    actual_str, expected_str, test_name=f"TC_PNEG_001 - {field_name}"
                )
                raise AssertionError(
                    f"{field_name} mismatch → Expected: '{expected_str}', Got: '{actual_str}'"
                )
            else:
                print_result(
                    actual_str, expected_str, test_name=f"TC_PNEG_001 - {field_name}"
                )
        
        time.sleep(1)
        row_tds = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table[@class='koptable']//tbody/tr[1]/td")
            )
        )

        status_from_table = row_tds[8].text
        if status_from_table.lower().startswith("lainnya:"):
            status_from_table = status_from_table[len("Lainnya:") :].strip()
        status_from_table = re.sub(r"^\d+\.\s*", "", status_from_table).strip()
        
        try:
            check_or_fail("Penyebab Penyerahan Pengembalian", penyebab, row_tds[10].text)
            check_or_fail("No BAST", no_bast, row_tds[11].text)
            check_or_fail("Tgl BAST", tgl_bast, row_tds[12].text)

            print_result(1, 1, test_name="TC_PNPE_001")
            
            time.sleep(3)

        except AssertionError:
            return

    # @unittest.skip("Belum mau dijalankan sekarang")
    def test_TC_PNPE_002(self):
        print("test_TC_PNPE_002")
        driver = self.driver
        tc_pnbk = self.tc_pnbk

        driver.find_element(By.CSS_SELECTOR, "#fmpenyebab_pengembalian > option:nth-child(1)").click()
        driver.find_element(By.ID, "fmno_bast").clear()
        driver.find_element(By.ID, "fmtgl_bast").clear()
        clear_readonly_input(driver, By.ID, "fmpenerima_nama")
        driver.find_element(By.ID, "fmpenerima_pangkat").clear()
        driver.find_element(By.CSS_SELECTOR, "#fmkondisi > option:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, "#fmdiinput_oleh > option:nth-child(1)").click()
        clear_readonly_input(driver, By.ID, "fmdiinput_nama")
        
        save_get_alert(
            driver,
            expected="Penyebab Pengembalian belum diisi!",
            test_name="TC_PNPE_004"
        )
        
        tc_pnbk.test_TC_PNBK_002(isedit=True)
        tc_pnbk.test_TC_PNBK_003(isedit=True)
        tc_pnbk.test_TC_PNBK_004(isedit=True)
        tc_pnbk.test_TC_PNBK_005(isedit=True)
        tc_pnbk.test_TC_PNBK_006(isedit=True)
        tc_pnbk.test_TC_PNBK_007(isedit=True)
        tc_pnbk.test_TC_PNBK_008(isedit=True)
        tc_pnbk.test_TC_PNBK_009(isedit=True)
        tc_pnbk.test_TC_PNBK_010(isedit=True)
        tc_pnbk.test_TC_PNBK_011(isedit=True)
        tc_pnbk.test_TC_PNBK_012(isedit=True)
        tc_pnbk.test_TC_PNBK_013(isedit=True)
        tc_pnbk.test_TC_PNBK_014(isedit=True)
        tc_pnbk.test_TC_PNBK_015(isedit=True)
        # tc_pnbk.test_TC_PNBK_016(isedit=True)
        
    def test_TC_PNPE_003(self):
        print("TC_PNPE_003")
        data = self.__class__.shared
        actual = nama_pemakai_check(self)
        expected = data.get("nama_pemakai", "")
        print_result(actual, expected, test_name="TC_PNPE_003")


if __name__ == "__main__":
    unittest.main(defaultTest="TC_PNPE")
