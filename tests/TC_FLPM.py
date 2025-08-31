import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from components.button import button
from components.dropdown import Dropdown
from components.form_input import form_input
from helpers.clear_readonly_input import clear_readonly_input
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time
import re


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

    #     @unittest.skip("untuk testing")
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
                    f"- Gagal di baris data ke-{idx}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmFiltNibar")

    #     @unittest.skip("untuk testing")
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

                if value == "80":
                    if actual_text not in ("Baik", "Rusak Berat"):
                        failed.append(
                            {"row": idx, "exp": "Baik/Rusak Berat", "act": actual_text}
                        )

                elif value == "81":
                    pass

                else:
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

    #     @unittest.skip("untuk testing")
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
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmKodeBarang")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_004(self):
        print("test_TC_FLPM_004")
        driver = self.driver

        names = ["suv", "motor"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[5]"

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, name):
                    mismatches.append((idx_row, name, actual, "mismatch nilai"))

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
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNamaBarang")

    #     @unittest.skip("untuk testing")
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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, merk):
                    mismatches.append((idx_row, merk, actual, "mismatch nilai"))

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
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmMerk")

    #     @unittest.skip("untuk testing")
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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, merk):
                    mismatches.append((idx_row, merk, actual, "mismatch nilai"))

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
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNoPolisi")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, merk):
                    mismatches.append((idx_row, merk, actual, "mismatch nilai"))

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
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNoBPKB")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_008(self):
        print("test_TC_FLPM_008")
        driver = self.driver

        no_mesins = ["DBB5445", "KC11E1159751", "E"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[12]"

        for i, no_mesin in enumerate(no_mesins, start=1):
            time.sleep(1)
            filter_pengamanan(driver, no_mesin, "fmNoMesin")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, no_mesin):
                    mismatches.append((idx_row, no_mesin, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(no_mesins), test_name="TC_FLPM_008")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNoMesin")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_009(self):
        print("test_TC_FLPM_009")
        driver = self.driver

        no_rangkas = ["MHFE2CJ3C8K014559", "MHFM1CA4-J9K-020563	", "E"]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[11]"

        for i, no_rangka in enumerate(no_rangkas, start=1):
            time.sleep(1)
            filter_pengamanan(driver, no_rangka, "fmNoRangka")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, no_rangka):
                    mismatches.append((idx_row, no_rangka, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(no_rangkas), test_name="TC_FLPM_009")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNoRangka")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_010(self):
        print("test_TC_FLPM_010")
        driver = self.driver

        no_pabriks = [
            "CU-PC9CKH",
            "S/N : PTSB-90931 E 2702 ( CPU ) S/N: ETLB 29A 3400",
            "E",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[10]"

        for i, no_pabrik in enumerate(no_pabriks, start=1):
            time.sleep(1)
            filter_pengamanan(driver, no_pabrik, "fmNoPabrik")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, no_pabrik):
                    mismatches.append((idx_row, no_pabrik, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(no_pabriks), test_name="TC_FLPM_010")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmNoPabrik")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_011(self):
        print("test_TC_FLPM_011")
        driver = self.driver

        bahans = [
            "besi",
            "campuran",
            "E",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[8]"

        for i, bahan in enumerate(bahans, start=1):
            time.sleep(1)
            filter_pengamanan(driver, bahan, "fmBahan")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, bahan):
                    mismatches.append((idx_row, bahan, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(bahans), test_name="TC_FLPM_011")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmBahan")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_012(self):
        print("test_TC_FLPM_012")
        driver = self.driver

        keterangans = [
            "Keg. Pembinaan Usaha Petamb. (APBD)",
            "Mesin Pemotong Batu",
            "E",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[18]"

        for i, keterangan in enumerate(keterangans, start=1):
            time.sleep(1)
            filter_pengamanan(driver, keterangan, "fmFiltKeterangan")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, keterangan):
                    mismatches.append((idx_row, keterangan, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(keterangans), test_name="TC_FLPM_012")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmFiltKeterangan")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_013(self):
        print("test_TC_FLPM_013")
        driver = self.driver

        nama_pemakais = [
            "luki",
            "E",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[19]"

        for i, nama_pemakai in enumerate(nama_pemakais, start=1):
            time.sleep(1)
            filter_pengamanan(driver, nama_pemakai, "fmFiltNamaPemakai")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, nama_pemakai):
                    mismatches.append((idx_row, nama_pemakai, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(nama_pemakais), test_name="TC_FLPM_013")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmFiltNamaPemakai")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_014(self):
        print("test_TC_FLPM_014")
        driver = self.driver

        no_identitas_pemakais = [
            "12345678",
            "E",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[19]"

        for i, no_identitas_pemakai in enumerate(no_identitas_pemakais, start=1):
            time.sleep(1)
            filter_pengamanan(driver, no_identitas_pemakai, "fmFiltNoIdentitasPemakai")

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                if not self.is_found(actual, no_identitas_pemakai):
                    mismatches.append(
                        (idx_row, no_identitas_pemakai, actual, "mismatch nilai")
                    )

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(no_identitas_pemakais), test_name="TC_FLPM_014")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmFiltNoIdentitasPemakai")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_015(self):
        print("test_TC_FLPM_015")
        driver = self.driver

        no_basts = [
            "08/bast/2025",
            "b",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[17]"

        for i, no_bast in enumerate(no_basts, start=1):
            time.sleep(1)
            filter_pengamanan(driver, no_bast, "fmFiltNoBAST")

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
                    raw_text = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue

                lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
                actual = lines[1] if len(lines) > 1 else lines[0] if lines else ""

                if not self.is_found(actual, no_bast):
                    mismatches.append((idx_row, no_bast, actual, "mismatch nilai"))

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(no_basts), test_name="TC_FLPM_015")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmFiltNoBAST")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_016(self):
        driver = self.driver

        dropdown_locator = (By.ID, "fmFiltStatusPengamanan")
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

            status_list = driver.find_elements(
                By.XPATH, "//table[@class='koptable']//tbody//tr[@id]/td[19]"
            )

            if not status_list:
                print(f"ℹ️ Tidak ada data untuk filter '{label}'.")
                continue

            for idx, el in enumerate(status_list, start=1):
                actual_text = el.text.strip()

                if value == "1":
                    if actual_text == "/\n/":
                        failed.append(
                            {"row": idx, "exp": "≠ '/\\n/'", "act": actual_text}
                        )

                elif value == "2":
                    if actual_text != "/\n/":
                        failed.append(
                            {"row": idx, "exp": "'/\\n/'", "act": actual_text}
                        )

                else:
                    if actual_text != label:
                        failed.append({"row": idx, "exp": label, "act": actual_text})

        if failed:
            test_pass = False

        print_result(test_pass, True, "TC_FLPM_016")

        if not test_pass:
            for f in failed:
                print(
                    f"- Gagal di filter [{f['exp']}] baris ke-{f['row']} → Expected: '{f['exp']}', Actual: '{f['act']}'"
                )
            print(
                "========================================================================"
            )
        Dropdown(driver, identifier="fmKondisiBarang", value="__reset__")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_017(self):
        print("test_TC_FLPM_017")
        driver = self.driver

        tahun_bukus = [
            "2015",
            "2017",
            "2025",
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[17]"

        for i, tahun_buku in enumerate(tahun_bukus, start=1):
            time.sleep(1)
            filter_pengamanan(driver, tahun_buku, "fmTahunBuku")

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
                    raw_text = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue
                first_line = next(
                    (line.strip() for line in raw_text.splitlines() if line.strip()), ""
                )
                m = re.search(r"\b\d{2}-\d{2}-(\d{4})\b", first_line)
                actual_year = m.group(1) if m else ""
                if actual_year != tahun_buku:
                    mismatches.append(
                        (
                            idx_row,
                            tahun_buku,
                            first_line,
                            f"tahun '{actual_year}' tidak sesuai",
                        )
                    )
            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(tahun_bukus), test_name="TC_FLPM_017")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmTahunBuku")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_018(self):
        print("test_TC_FLPM_018")
        driver = self.driver

        tahun_perolehans = [
            ("2015", "2020"),
            ("2017", "2019"),
            ("2024", "2025"),
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[9]"

        for i, (start, end) in enumerate(tahun_perolehans, start=1):
            time.sleep(1)
            self.filter_range(
                start, "fmTahunPerolehanAwal", end, "fmTahunPerolehanAkhir"
            )

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue
                if not (
                    (
                        fl := next(
                            (
                                line.strip()
                                for line in actual.splitlines()
                                if line.strip()
                            ),
                            "",
                        )
                    )
                    and (m := re.search(r"\b(?:19|20)\d{2}\b", fl))
                    and (int(start.strip()) <= int(m.group(0)) <= int(end.strip()))
                ):
                    mismatches.append(
                        (idx_row, f"{start}-{end}", fl, "tahun di luar rentang")
                    )

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(tahun_perolehans), test_name="TC_FLPM_018")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAwal")
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAkhir")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_019(self):
        print("test_TC_FLPM_019")
        driver = self.driver

        harga_perolehans = [
            ("2000000", "3000000"),
            ("100000000", "200000000"),
            ("100000", "500000"),
        ]

        success_cases = 0
        failed = []

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        cell_kode_xpath = "./td[16]"

        for i, (start, end) in enumerate(harga_perolehans, start=1):
            time.sleep(1)
            self.filter_range(
                start, "fmHargaPerolehanAwal", end, "fmHargaPerolehanAkhir"
            )

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
                    actual = (td.get_attribute("innerText") or "").strip()
                except NoSuchElementException:
                    continue
                fl = next(
                    (line.strip() for line in actual.splitlines() if line.strip()), ""
                )
                m = re.search(r"(?i)(?:rp\s*)?([\d][\d\.\,\s]*)", fl)

                price = None
                if m:
                    num = re.sub(r"[^\d.,]", "", m.group(1))
                    if "," in num and "." in num:
                        price = int(float(num.replace(".", "").replace(",", ".")))
                    elif "." in num:
                        price = int(num.replace(".", ""))
                    elif "," in num:
                        price = int(float(num.replace(",", ".")))
                    else:
                        price = int(num)

                if price is None or not (int(start) <= price <= int(end)):
                    mismatches.append(
                        (idx_row, f"{start}-{end}", fl, "harga di luar rentang")
                    )

            if mismatches:
                failed.extend(
                    [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
                )
            else:
                success_cases += 1

        print_result(success_cases, len(harga_perolehans), test_name="TC_FLPM_019")

        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal di baris data ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(driver, By.ID, "fmHargaPerolehanAwal")
        clear_readonly_input(driver, By.ID, "fmHargaPerolehanAkhir")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_020(self):
        print("test_TC_FLPM_020")

        driver = self.driver

        dropdown_locator = (By.ID, "fmOrder")
        dropdown = Select(driver.find_element(*dropdown_locator))

        options_data = []
        for opt in dropdown.options:
            val = opt.get_attribute("value")
            if not val:
                continue
            options_data.append((val, (opt.text or "").strip()))

        failed = []
        test_pass = True

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"

        def first_non_empty_line(text: str) -> str:
            for line in (text or "").splitlines():
                s = line.strip()
                if s:
                    return s
            return ""

        def code_key(raw: str):
            s = first_non_empty_line(raw).rstrip("/")
            parts = [p for p in s.split(".") if p != ""]
            key = []
            for p in parts:
                try:
                    key.append(int(p))
                except ValueError:
                    key.append(float("inf"))
            return tuple(key), s + "/"

        for i, (value, label) in enumerate(options_data, start=1):
            print(f"🔎 Filter ke-{i}: {label} (value={value})")

            Select(driver.find_element(*dropdown_locator)).select_by_value(value)

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            form_input(self.driver, By.ID, "jmlperpage", "100")
            button(driver, By.ID, "btTampil")

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, data_row_xpath)),
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

            rows = driver.find_elements(By.XPATH, data_row_xpath)
            if not rows:
                print(f"ℹ️ Tidak ada data untuk filter '{label}'.")
                continue

            if value == "1":
                values = []
                for idx_row, row in enumerate(rows, start=1):
                    try:
                        td = row.find_element(By.XPATH, "./td[3]")
                        raw = (td.get_attribute("innerText") or "").strip()
                        key, disp = code_key(raw)
                        values.append((idx_row, key, disp))
                    except NoSuchElementException:
                        continue

                for j in range(1, len(values)):
                    _, prev_key, prev_disp = values[j - 1]
                    cur_idx, cur_key, cur_disp = values[j]
                    if cur_key < prev_key:
                        failed.append(
                            {"row": cur_idx, "exp": f">= {prev_disp}", "act": cur_disp}
                        )

            elif value == "2":
                values = []
                for idx_row, row in enumerate(rows, start=1):
                    try:
                        td = row.find_element(By.XPATH, "./td[9]")
                        raw = (td.get_attribute("innerText") or "").strip()
                    except NoSuchElementException:
                        continue
                    m = re.search(r"\b(?:19|20)\d{2}\b", raw)
                    year = int(m.group(0)) if m else None
                    values.append((idx_row, year, raw))

                for j in range(1, len(values)):
                    _, prev_year, _ = values[j - 1]
                    cur_idx, cur_year, cur_raw = values[j]
                    if cur_year is None or prev_year is None or cur_year < prev_year:
                        failed.append(
                            {
                                "row": cur_idx,
                                "exp": f">= {prev_year if prev_year is not None else 'YYYY'}",
                                "act": cur_raw,
                            }
                        )
            else:
                pass

            if failed:
                test_pass = False

        print_result(test_pass, True, "TC_FLPM_020")
        if not test_pass:
            for f in failed:
                print(
                    f"- Gagal di filter [{f['exp']}] baris ke-{f['row']} → Expected: '{f['exp']}', Actual: '{f['act']}'"
                )
            print(
                "========================================================================"
            )
        Dropdown(driver, identifier="fmOrder", value="__reset__")
        clear_readonly_input(self.driver, By.ID, "jmlperpage")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_021(self):
        print("test_TC_FLPM_021")
        driver = self.driver

        per_pages = ["10", "25", "50", "100"]

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        nodata_xpath = "//*[contains(translate(., 'TIDAK ADA DATA', 'tidak ada data'), 'tidak ada data') or contains(., 'No data')]"

        success_cases = 0
        failed = []

        for i, per_page in enumerate(per_pages, start=1):
            print(f"🔎 Kasus ke-{i}: jml per page = {per_page}")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
            except Exception:
                old_tbody = None

            form_input(driver, By.ID, "jmlperpage", str(per_page))
            button(driver, By.ID, "btTampil")

            try:
                if old_tbody:
                    self.wait.until(EC.staleness_of(old_tbody))
            except TimeoutException:
                pass

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css))
            )
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, data_row_xpath)),
                        EC.presence_of_element_located((By.XPATH, nodata_xpath)),
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//table[@class='koptable']//tbody//tr[td[contains(.,'Total')]]",
                            )
                        ),
                    )
                )
            except TimeoutException:
                pass

            rows = driver.find_elements(By.XPATH, data_row_xpath)
            count = len(rows)
            expected = int(per_page)

            if count == 0:
                print(f"ℹ️ Tidak ada data (0 ≤ {expected}) → dianggap sesuai.")
                success_cases += 1
                continue

            if count <= expected:
                print(f"✅ OK: {count} baris (≤ {expected})")
                success_cases += 1
            else:
                failed.append({"case": i, "exp": f"≤ {expected}", "act": f"{count}"})

        print_result(success_cases, len(per_pages), test_name="TC_FLPM_021")

        if failed:
            for f in failed:
                print(
                    f"- Gagal di kasus ke-{f['case']}: jumlah baris melebihi per page → Expected: '{f['exp']}', Actual: '{f['act']}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(self.driver, By.ID, "jmlperpage")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_022(self):
        print("test_TC_FLPM_022")
        import re

        driver = self.driver

        tbody_css = "table.koptable tbody"
        data_row_xpath = "//table[@class='koptable']//tbody//tr[@id]"
        price_cell_xpath = "./td[16]"
        total_row_xpath = "//table[@class='koptable']//tbody//tr[td//b[contains(normalize-space(),'Total per Halaman')]]"
        total_cell_xpath = (
            total_row_xpath
            + "/td[.//b[contains(normalize-space(),'Total per Halaman')]]/following-sibling::td[1]"
        )
        nodata_xpath = (
            "//*[contains(translate(., 'TIDAK ADA DATA', 'tidak ada data'), 'tidak ada data') "
            "or contains(., 'No data')]"
        )

        def parse_rupiah(s: str) -> int:
            """Parse angka format ID ('.' ribuan, ',' desimal) ke int rupiah."""
            if not s:
                return 0
            s = s.strip()
            s = re.sub(r"(?i)rp\s*", "", s)
            s = re.sub(r"[^\d.,]", "", s)
            if "," in s and "." in s:
                return int(float(s.replace(".", "").replace(",", ".")))
            if "." in s and "," not in s:
                return int(s.replace(".", ""))
            if "," in s and "." not in s:
                return int(float(s.replace(",", ".")))
            return int(s)

        try:
            old_tbody = driver.find_element(By.CSS_SELECTOR, tbody_css)
        except Exception:
            old_tbody = None

        try:
            if old_tbody:
                self.wait.until(EC.staleness_of(old_tbody))
        except TimeoutException:
            pass

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tbody_css)))
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, data_row_xpath)),
                    EC.presence_of_element_located((By.XPATH, total_row_xpath)),
                    EC.presence_of_element_located((By.XPATH, nodata_xpath)),
                )
            )
        except TimeoutException:
            pass

        rows = driver.find_elements(By.XPATH, data_row_xpath)

        computed_sum = 0
        for idx_row, row in enumerate(rows, start=1):
            try:
                td = row.find_element(By.XPATH, price_cell_xpath)
            except NoSuchElementException:
                continue
            raw = (td.get_attribute("innerText") or "").strip()
            amount = parse_rupiah(raw)
            computed_sum += amount
            print(f"➕ Row {idx_row}: {raw} -> {amount:,}")

        try:
            total_el = driver.find_element(By.XPATH, total_cell_xpath)
        except NoSuchElementException:
            try:
                total_el = driver.find_element(By.XPATH, total_row_xpath + "/td[2]")
            except NoSuchElementException:
                total_el = None

        if total_el is not None:
            total_text = (total_el.get_attribute("innerText") or "").strip()
            displayed_total = parse_rupiah(total_text)
        else:
            total_text = ""
            displayed_total = None

        print(
            f"Σ Computed: {computed_sum:,} | Display: {displayed_total if displayed_total is not None else 'N/A'} ({total_text})"
        )

        if len(rows) == 0:
            test_pass = displayed_total in (None, 0)
        else:
            test_pass = displayed_total is not None and computed_sum == displayed_total

        print_result(test_pass, True, "TC_FLPM_022")

        if not test_pass:
            reason = (
                "Total per Halaman tidak ditemukan"
                if displayed_total is None
                else "Jumlah tidak sama"
            )
            print(
                f"- Gagal: {reason} → Expected sum: '{computed_sum:,}', Actual: '{total_text}'"
            )
            print(
                "========================================================================"
            )

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_023(self):
        print("test_TC_FLPM_023")
        driver = self.driver
        form_input(driver, By.ID, "fmFiltNibar", TC_FLPM.nibar)
        time.sleep(1)
        Dropdown(driver, identifier="fmKondisiBarang", value="1")
        time.sleep(1)
        kode_barang = "1.3.2.02.01.01.005"
        form_input(driver, By.ID, "fmKodeBarang", kode_barang)
        time.sleep(1)
        nama_barang = "SUV"
        form_input(driver, By.ID, "fmNamaBarang", nama_barang)
        time.sleep(1)
        merk = "Toyota"
        form_input(driver, By.ID, "fmMerk", merk)
        time.sleep(1)
        no_pol = "A 662"
        form_input(driver, By.ID, "fmNoPolisi", no_pol)
        time.sleep(1)
        no_bpkb = "F 4032561"
        form_input(driver, By.ID, "fmNoBPKB", no_bpkb)
        time.sleep(1)
        no_mesin = "DBB5445"
        form_input(driver, By.ID, "fmNoMesin", no_mesin)
        time.sleep(1)
        no_rangka = "MHFE2CJ3C8K014559"
        form_input(driver, By.ID, "fmNoRangka", no_rangka)
        time.sleep(1)
        bahan = "campuran"
        form_input(driver, By.ID, "fmBahan", bahan)
        time.sleep(1)
        no_pabrik = ""
        form_input(driver, By.ID, "fmNoPabrik", no_pabrik)
        time.sleep(1)
        keterangan = "Pengadaan"
        form_input(driver, By.ID, "fmFiltKeterangan", keterangan)
        time.sleep(1)
        nama_pemakai = "luki"
        form_input(driver, By.ID, "fmFiltNamaPemakai", nama_pemakai)
        time.sleep(1)
        no_identitas_pemakai = "12345678"
        form_input(driver, By.ID, "fmFiltNoIdentitasPemakai", no_identitas_pemakai)
        time.sleep(1)
        Dropdown(driver, identifier="fmFiltStatusPengamanan", value="1")
        time.sleep(1)
        tahun_buku = "2008"
        form_input(driver, By.ID, "fmTahunBuku", tahun_buku)
        time.sleep(1)
        tahun_perolehan = ["2008", "2010"]
        self.filter_range(
            tahun_perolehan[0],
            "fmTahunPerolehanAwal",
            tahun_perolehan[1],
            "fmTahunPerolehanAkhir",
        )
        time.sleep(1)
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.koptable tbody"))
        )
        row = driver.find_elements(
            By.XPATH, "//table[@class='koptable']//tbody//tr[@id]"
        )

        print_result(True, bool(row), test_name="TC_FLPM_023")
        clear_readonly_input(driver, By.ID, "fmFiltNibar")
        Dropdown(driver, identifier="fmKondisiBarang", value="__reset__")
        clear_readonly_input(driver, By.ID, "fmKodeBarang")
        clear_readonly_input(driver, By.ID, "fmMerk")
        clear_readonly_input(driver, By.ID, "fmNoPolisi")
        clear_readonly_input(driver, By.ID, "fmNoBPKB")
        clear_readonly_input(driver, By.ID, "fmNoMesin")
        clear_readonly_input(driver, By.ID, "fmNoRangka")
        clear_readonly_input(driver, By.ID, "fmNoPabrik")
        clear_readonly_input(driver, By.ID, "fmBahan")
        clear_readonly_input(driver, By.ID, "fmFiltNamaPemakai")
        clear_readonly_input(driver, By.ID, "fmFiltNoIdentitasPemakai")
        Dropdown(driver, identifier="fmFiltStatusPengamanan", value="__reset__")
        clear_readonly_input(driver, By.ID, "fmTahunBuku")
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAwal")
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAkhir")

    #     @unittest.skip("untuk testing")
    def test_TC_FLPM_024(self):
        print("test_TC_FLPM_024")
        self.test_TC_FLPM_001()
        self.test_TC_FLPM_002()
        self.test_TC_FLPM_003()
        self.test_TC_FLPM_004()
        self.test_TC_FLPM_005()
        self.test_TC_FLPM_006()
        self.test_TC_FLPM_007()
        self.test_TC_FLPM_008()
        self.test_TC_FLPM_009()
        self.test_TC_FLPM_010()
        self.test_TC_FLPM_011()
        self.test_TC_FLPM_012()
        self.test_TC_FLPM_013()
        self.test_TC_FLPM_014()
        self.test_TC_FLPM_015()
        self.test_TC_FLPM_016()
        self.test_TC_FLPM_017()
        self.test_TC_FLPM_018()
        self.test_TC_FLPM_019()
        self.test_TC_FLPM_020()
        self.test_TC_FLPM_021()
        self.test_TC_FLPM_022()
        self.test_TC_FLPM_023()
        self.test_TC_FLPM_024()

    def is_found(self, actual: str | None, name: str | None) -> bool:
        if not actual or not name:
            return False
        return name.lower() in actual.strip().lower()

    def filter_range(self, start, locator_start, end, locator_end, submit=True):
        form_input(self.driver, By.ID, locator_start, start)
        time.sleep(1)
        form_input(self.driver, By.ID, locator_end, end)
        time.sleep(1)
        if submit:
            button(self.driver, By.ID, "btTampil")


if __name__ == "__main__":
    unittest.main()
