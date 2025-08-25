import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from components.button import button
from components.dropdown import Dropdown
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time


class TC_FLPM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_FLPM.nibar = os.getenv("nibar")
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananPeralatan")
        time.sleep(1)
        cls.wait = WebDriverWait(driver, 10)

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

    @unittest.skip("untuk testing")
    def test_TC_FLPM_001(self):
        print("test_TC_FLPM_001")
        driver = self.driver
        nibar_list = ["167192", "167193", "100000"]

        success = 0
        failed = []

        for i, nibar in enumerate(nibar_list, start=1):
            time.sleep(1)
            filter_pengamanan(driver, text=nibar)

            expected = nibar.strip()
            xpath = f'//table[@class="koptable"]//a[normalize-space()="{expected}"]'

            try:
                elem = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                actual = (elem.text or "").strip()
                if actual == expected:
                    success += 1
                else:
                    failed.append((i, expected, actual, "mismatch nilai"))
            except TimeoutException:
                failed.append(
                    (i, expected, "NOT FOUND", "tidak ditemukan di tabel (Timeout)")
                )

        print_result(success, len(nibar_list), test_name="TC_FLPM_001")

        if failed:
            for idx, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "")

    @unittest.skip("untuk testing")
    def test_TC_FLPM_002(self):
        driver = self.driver

        dropdown_locator = (By.ID, "fmKondisiBarang")
        dropdown = Select(driver.find_element(*dropdown_locator))

        options_data = []
        for opt in dropdown.options:
            val = opt.get_attribute("value")
            if not val:
                continue
            options_data.append((val, (opt.text or "").strip()))

        failed = []
        test_pass = True

        for i, (value, label) in enumerate(options_data, start=1):
            print(f"🔎 Filter ke-{i}: {label} (value={value})")

            Select(driver.find_element(*dropdown_locator)).select_by_value(value)

            old_tbody = driver.find_element(
                By.XPATH, "//table[@class='koptable']//tbody"
            )

            button(driver, By.ID, "btTampil")

            try:
                self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "table.koptable tbody")
                )
            )

            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located(
                            (By.XPATH, "//table[@class='koptable']//tbody//tr[@id]")
                        ),
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//table[@class='koptable']//tbody//tr[td[contains(.,'Total')]]",
                            )
                        ),
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(translate(., 'TIDAK ADA DATA', 'tidak ada data'), 'tidak ada data') or contains(., 'No data')]",
                            )
                        ),
                    )
                )
            except TimeoutException:
                pass

            kondisi_list = driver.find_elements(
                By.XPATH, "//table[@class='koptable']//tbody//tr[@id]/td[15]"
            )

            if not kondisi_list:
                print(f"ℹ️ Tidak ada data untuk filter '{label}'.")
                continue

            for idx, el in enumerate(kondisi_list, start=1):
                actual_text = el.text.strip()
                if actual_text != label:
                    failed.append({"row": idx, "exp": label, "act": actual_text})

        if failed:
            test_pass = False

        print_result(test_pass, True, "TC_FLPM_002")

        if not test_pass:
            for f in failed:
                print(
                    f"- Gagal di filter [{f['exp']}] baris ke-{f['row']} → Expected: '{f['exp']}', Actual: '{f['act']}'"
                )
            print(
                "========================================================================"
            )
        Dropdown(driver, identifier="fmKondisiBarang", value="__reset__")

    @unittest.skip("untuk testing")
    def test_TC_FLPM_003(self):
        print("test_TC_FLPM_003")
        driver = self.driver

        codes = ["1.3.2.13.03.01.001", "1.3.2.01.03.04.001"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[3]"

        for i, code in enumerate(codes, start=1):
            filter_pengamanan(driver, code, "fmKodeBarang")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )

            rows = driver.find_elements(By.XPATH, data_row_xpath)

            if not rows:
                failed.append(
                    (i, code, "NOT FOUND", "tidak ditemukan di tabel (kosong)")
                )
                continue

            def parse_kode(td_text: str | None) -> str:
                text = td_text or ""
                first_line = text.split("\n")[0]
                return first_line.split("/")[0].strip()

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                td = row.find_element(By.XPATH, cell_kode_xpath)
                actual_kode = parse_kode(td.get_attribute("innerText"))
                if actual_kode != code:
                    mismatches.append((idx_row, code, actual_kode, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(codes), test_name="TC_FLPM_003")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "", "fmKodeBarang")

    @unittest.skip("untuk testing")
    def test_TC_FLPM_004(self):
        print("test_TC_FLPM_004")
        driver = self.driver

        names = ["suv", "motor"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[5]"

        def is_found(actual_name: str | None, name: str | None) -> bool:
            if not actual_name or not name:
                return False
            return name.lower() in actual_name.strip().lower()

        for i, name in enumerate(names, start=1):
            time.sleep(1)
            filter_pengamanan(driver, name, "fmNamaBarang")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            rows = driver.find_elements(By.XPATH, data_row_xpath)

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                try:
                    td = row.find_element(By.XPATH, cell_kode_xpath)
                    actual_name = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual_name, name):
                    mismatches.append((idx_row, name, actual_name, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(names), test_name="TC_FLPM_004")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "", "fmNamaBarang")

    @unittest.skip("untuk testing")
    def test_TC_FLPM_005(self):
        print("test_TC_FLPM_005")
        driver = self.driver

        types = ["toyota", "honda"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[6]"

        for i, merk in enumerate(types, start=1):
            time.sleep(1)
            filter_pengamanan(driver, merk, "fmMerk")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            rows = driver.find_elements(By.XPATH, data_row_xpath)

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                try:
                    td = row.find_element(By.XPATH, cell_kode_xpath)
                    actual_name = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual_name, merk):
                    mismatches.append((idx_row, merk, actual_name, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(types), test_name="TC_FLPM_005")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "", "fmMerk")

    @unittest.skip("untuk testing")
    def test_TC_FLPM_006(self):
        print("test_TC_FLPM_006")
        driver = self.driver

        types = ["A 662", "B"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[13]"

        for i, merk in enumerate(types, start=1):
            time.sleep(1)
            filter_pengamanan(driver, merk, "fmNoPolisi")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            rows = driver.find_elements(By.XPATH, data_row_xpath)

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                try:
                    td = row.find_element(By.XPATH, cell_kode_xpath)
                    actual_name = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual_name, merk):
                    mismatches.append((idx_row, merk, actual_name, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(types), test_name="TC_FLPM_006")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "", "fmNoPolisi")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_007(self):
        print("test_TC_FLPM_007")
        driver = self.driver

        types = ["F 4032561", "E"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[14]"

        for i, merk in enumerate(types, start=1):
            time.sleep(1)
            filter_pengamanan(driver, merk, "fmNoBPKB")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            rows = driver.find_elements(By.XPATH, data_row_xpath)

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                try:
                    td = row.find_element(By.XPATH, cell_kode_xpath)
                    actual_name = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual_name, merk):
                    mismatches.append((idx_row, merk, actual_name, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(types), test_name="TC_FLPM_007")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di kasus ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        filter_pengamanan(driver, "", "fmNoBPKB")

    def is_found(self, actual_name: str | None, name: str | None) -> bool:
        if not actual_name or not name:
            return False
        return name.lower() in actual_name.strip().lower()


DBB5445
if __name__ == "__main__":
    unittest.main()
