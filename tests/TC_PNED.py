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

from tests.TC_PNBR import TC_PNBR


class TC_PNED(unittest.TestCase):
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
        TC_PNED.nibar = os.getenv("nibar")
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananPeralatanTrans")
        time.sleep(1)
        cls.shared = {}
        cls.tc_pnbr = TC_PNBR()
        cls.tc_pnbr.driver = cls.driver

    @classmethod
    def tearDownClass(cls):
        #         try:
        #             logout(cls.driver)
        #         except Exception as e:
        #             print(f"⚠️ Logout gagal: {e}")
        #         finally:
        #             cls.driver.quit()
        #
        cls.driver.quit()

    def setUp(self):
        if self._testMethodName in ["test_TC_PNED_001", "test_TC_PNED_002"]:
            filter_pengamanan(self.driver, TC_PNED.nibar or "")
            time.sleep(1)
            checkbox(
                self.driver, identifier=1, by="index", table_selector="table.koptable"
            )
            time.sleep(1)
            href_button(self.driver, "javascript:pengamananPeralatanTrans.formEdit()")
            time.sleep(1)

    def _dismiss_if_alert(self, driver):
        try:
            driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        except Exception:
            pass

    #     @unittest.skip("Belum mau dijalankan sekarang")
    def test_TC_PNED_001(self):
        print("test_TC_PNED_001")
        driver = self.driver

        def _norm(s: str) -> str:
            return " ".join(s.split()).strip()

        button(driver, By.ID, "fmnama_pemakai_button")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#PegawaiPilih_cont_daftar > table tbody tr")
            )
        )

        target_index = 2
        checkbox(
            driver,
            identifier=target_index,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )
        rows = driver.find_elements(
            By.CSS_SELECTOR, "#PegawaiPilih_cont_daftar > table tbody tr"
        )
        expected_name = (
            rows[target_index].find_elements(By.TAG_NAME, "td")[3].text.strip()
        )

        driver.execute_script("PegawaiPilih.windowSave();")

        def value_equals_expected(d):
            el = d.find_element(By.ID, "fmnama_pemakai")
            return _norm(el.get_attribute("value")) == _norm(expected_name)

        nama_pemakai = ""
        try:
            WebDriverWait(driver, 2).until(value_equals_expected)
        except Exception:
            nama_pemakai = (
                driver.find_element(By.ID, "fmnama_pemakai").get_attribute("value")
                or ""
            ).strip()
        self.__class__.shared["nama_pemakai"] = nama_pemakai

        time.sleep(1)
        status_value = "3"
        Dropdown(driver, identifier="fmstatus_pemakai", value=status_value, by="id")

        if status_value == "5":
            self._dismiss_if_alert(driver)
            status_lainnya = "pimpinan divisi"
            form_input(driver, By.ID, "fmstatus_pemakai_lainnya", status_lainnya)
            time.sleep(1)
        else:
            selected_option = Select(
                driver.find_element(By.ID, "fmstatus_pemakai")
            ).first_selected_option
            status_lainnya = selected_option.text.strip()

        time.sleep(1)
        no_ktp = "098765"
        form_input(driver, By.ID, "fmno_ktp_pemakai", no_ktp)

        time.sleep(1)
        alamat_pemakai = "bandung"
        form_input(driver, By.ID, "fmalamat_pemakai", alamat_pemakai)

        time.sleep(1)
        no_bast = "07/bast/2025"
        form_input(driver, By.ID, "fmno_bast", no_bast)

        time.sleep(1)
        tgl_bast = datetime.now().strftime("%d-%m-%Y")
        try:
            driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()
        except Exception:
            pass
        driver.find_element(By.ID, "fmtgl_bast").clear()
        driver.find_element(By.ID, "fmtgl_bast").send_keys(tgl_bast)

        time.sleep(1)
        diinput_oleh = "3"
        Dropdown(driver, identifier="fmdiinput_oleh", value=diinput_oleh, by="id")

        time.sleep(1)
        button(driver, By.ID, "fmdiinput_nama_button")

        time.sleep(1)
        checkbox(
            driver,
            identifier=1,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )

        time.sleep(1)
        driver.execute_script("PegawaiPilih.windowSave();")

        time.sleep(1)
        datepicker_trigger = driver.find_element(
            By.XPATH,
            "//input[@id='fmtgl_buku_tgl']/following-sibling::img[contains(@class,'ui-datepicker-trigger')]",
        )
        datepicker_trigger.click()
        set_tgl_buku(driver, tgl_bast)
        time.sleep(1)

        button(driver, By.ID, "btSimpan")
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table.koptable"))
        )
        WebDriverWait(driver, 15).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "table.koptable tbody tr"))
            > 0
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
                    actual_str, expected_str, test_name=f"TC_PNED_001 - {field_name}"
                )
                raise AssertionError(
                    f"{field_name} mismatch → Expected: '{expected_str}', Got: '{actual_str}'"
                )
            else:
                print_result(
                    actual_str, expected_str, test_name=f"TC_PNED_001 - {field_name}"
                )

        try:
            check_or_fail("Nama Pemakai", nama_pemakai, row_tds[7].text)
            check_or_fail("Status Pemakai", status_lainnya, status_from_table)
            check_or_fail("No KTP", no_ktp, row_tds[10].text)
            check_or_fail("Alamat", alamat_pemakai, row_tds[11].text)
            check_or_fail("No BAST", no_bast, row_tds[12].text)
            check_or_fail("Tgl BAST", tgl_bast, row_tds[13].text)

            print_result(1, 1, test_name="TC_PNED_001")

        except AssertionError:
            return

    def test_TC_PNED_002(self):
        driver = self.driver
        tc_pbnr = self.tc_pnbr
        print("TC_PNED_002")

        def recover_if_failed(actual):
            if not actual:
                checkbox(
                    driver, identifier=1, by="index", table_selector="table.koptable"
                )
                time.sleep(1)
                href_button(driver, "javascript:pengamananPeralatanTrans.formEdit()")
                time.sleep(1)
            return actual

        clear_readonly_input(driver, By.ID, "fmnama_pemakai")
        recover_if_failed(tc_pbnr.test_TC_PNBR_004(True))

        Dropdown(driver, identifier="fmstatus_pemakai", value="__reset__")
        self.__class__.shared["nama_pemakai"] = tc_pbnr.test_TC_PNBR_005(True)

        clear_readonly_input(driver, By.ID, "fmstatus_pemakai_lainnya")
        recover_if_failed(tc_pbnr.test_TC_PNBR_006(True))

        clear_readonly_input(driver, By.ID, "fmno_ktp_pemakai")
        recover_if_failed(tc_pbnr.test_TC_PNBR_007(True))

        clear_readonly_input(driver, By.ID, "fmalamat_pemakai")
        recover_if_failed(tc_pbnr.test_TC_PNBR_008(True))

        clear_readonly_input(driver, By.ID, "fmno_bast")
        recover_if_failed(tc_pbnr.test_TC_PNBR_009(True))

        clear_readonly_input(driver, By.ID, "fmtgl_bast")
        recover_if_failed(tc_pbnr.test_TC_PNBR_010(True))

        Dropdown(driver, identifier="fmdiinput_oleh", value="__reset__")
        recover_if_failed(tc_pbnr.test_TC_PNBR_011(True))

        clear_readonly_input(driver, By.ID, "fmdiinput_nama")
        recover_if_failed(tc_pbnr.test_TC_PNBR_012(True))

        recover_if_failed(tc_pbnr.test_TC_PNBR_013(True))

    #         recover_if_failed(tc_pbnr.test_TC_PNBR_015(True))

    #     @unittest.skip("Belum mau dijalankan sekarang")
    def test_TC_PNED_003(self):
        print("TC_PNED_003")
        data = self.__class__.shared
        actual = nama_pemakai_check(self)
        expected = data.get("nama_pemakai", "")
        print_result(actual, expected, test_name="TC_PNED_003")


if __name__ == "__main__":
    unittest.main(defaultTest="TC_PNED")
