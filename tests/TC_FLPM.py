from typing import Callable
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


TBODY_CSS = "table.koptable tbody"
DATA_ROW_XPATH = "//table[@class='koptable']//tbody//tr[@id]"


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
        cls.wait = WebDriverWait(driver, 5)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()

    #         cls.driver.quit()

    def test_TC_FLPM_001(self, test_name="TC_FLPM_001"):
        print("test_" + test_name)
        nibar_list = ["167192", "167193", "100000"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            nibar_list,
            test_name,
            "fmFiltNibar",
            line=2,
            column_idx=3,
            exact=True,
        )

    def test_TC_FLPM_002(self, test_name="TC_FLPM_002", col: str = "15"):
        print("test_" + test_name)
        driver = self.driver
        wait = self.wait

        if col == "6":

            def _pre(actual_raw: str) -> str:
                return get_actual_split(actual_raw, 5)
        else:

            def _pre(actual_raw: str) -> str:
                return actual_raw.strip()

        def _validator(value: str, label: str, actual: str) -> tuple[bool, str]:
            if value == "80":
                ok = actual in ("Baik", "Rusak Berat")
                return ok, "Baik/Rusak Berat"
            elif value == "81":
                return True, label
            else:
                ok = is_found(actual, label)
                return ok, label

        run_dropdown_filter_test(
            driver,
            wait,
            dropdown_id="fmKondisiBarang",
            cell_col_index=int(col),
            test_name=test_name,
            preprocess_actual=_pre,
            validator=_validator,
        )

    def test_TC_FLPM_003(self, test_name="TC_FLPM_003"):
        print("test_" + test_name)
        kode_barang_list = ["1.3.2.13.03.01.001", "1.3.2.01.03.04.001"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            kode_barang_list,
            test_name,
            "fmKodeBarang",
            column_idx=3,
            exact=True,
        )

    def test_TC_FLPM_004(self, test_name="TC_FLPM_004"):
        print("test_" + test_name)
        name_list = ["suv", "motor"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            name_list,
            test_name,
            "fmNamaBarang",
            column_idx=5,
        )

    def test_TC_FLPM_005(self, test_name="TC_FLPM_005", line=1):
        print("test_" + test_name)
        type_list = ["toyota", "honda"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            type_list,
            test_name,
            "fmMerk",
            column_idx=6,
            line=line,
        )

    def test_TC_FLPM_006(self, test_name="TC_FLPM_006", column=13, line=1):
        print("test_" + test_name)
        plate_list = ["A 662", "B"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            plate_list,
            test_name,
            "fmNoPolisi",
            column_idx=column,
            line=line,
        )

    def test_TC_FLPM_007(self):
        test_name = "TC_FLPM_007"
        print("test_" + test_name)
        bpkb_list = ["F 4032561", "E"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            bpkb_list,
            test_name,
            "fmNoBPKB",
            column_idx=14,
        )

    def test_TC_FLPM_008(self):
        test_name = "TC_FLPM_008"
        print("test_" + test_name)
        mesin_list = ["DBB5445", "KC11E1159751", "E"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            mesin_list,
            test_name,
            "fmNoMesin",
            column_idx=12,
        )

    def test_TC_FLPM_009(self):
        test_name = "TC_FLPM_009"
        print("test_" + test_name)
        rangka_list = ["MHFE2CJ3C8K014559", "MHFM1CA4-J9K-020563	", "E"]

        validate_by_filter_form(
            self.driver,
            self.wait,
            rangka_list,
            test_name,
            "fmNoRangka",
            column_idx=11,
        )

    def test_TC_FLPM_010(self):
        test_name = "TC_FLPM_010"
        print("test_" + test_name)
        pabrik_list = [
            "CU-PC9CKH",
            "S/N : PTSB-90931 E 2702 ( CPU ) S/N: ETLB 29A 3400",
            "E",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            pabrik_list,
            test_name,
            "fmNoPabrik",
            column_idx=10,
        )

    def test_TC_FLPM_011(self):
        test_name = "TC_FLPM_011"
        print("test_" + test_name)
        bahan_list = [
            "besi",
            "campuran",
            "E",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            bahan_list,
            test_name,
            "fmBahan",
            column_idx=8,
        )

    def test_TC_FLPM_012(self):
        test_name = "TC_FLPM_012"
        print("test_" + test_name)
        keterangan_list = [
            "Keg. Pembinaan Usaha Petamb. (APBD)",
            "Mesin Pemotong Batu",
            "E",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            keterangan_list,
            test_name,
            "fmFiltKeterangan",
            column_idx=18,
        )

    def test_TC_FLPM_013(self, test_name="TC_FLPM_013", column=19):
        print("test_" + test_name)
        nama_list = [
            "luki",
            "sapta",
            "E",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            nama_list,
            test_name,
            "fmFiltNamaPemakai",
            column_idx=column,
        )

    def test_TC_FLPM_014(self, test_name="TC_FLPM_014", column=19, line=2):
        print("test_" + test_name)
        no_identitas_list = [
            "12345678",
            "E",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            no_identitas_list,
            test_name,
            "fmFiltNoIdentitasPemakai",
            line=line,
            column_idx=column,
            exact=True,
        )

    def test_TC_FLPM_015(self, test_name="TC_FLPM_015", column=19, line=3):
        print("test_" + test_name)
        no_bast_list = [
            "08/bast/2025",
            "b",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            no_bast_list,
            test_name,
            "fmFiltNoBAST",
            line=line,
            column_idx=column,
        )

    def test_TC_FLPM_016(self):
        test_name = "TC_FLPM_015"
        print("test_" + test_name)
        driver = self.driver
        wait = self.wait

        def _pre(actual_raw: str) -> str:
            return actual_raw.strip()

        def _validator(value: str, label: str, actual: str) -> tuple[bool, str]:
            sentinel = "/\n/"
            if value == "1":
                ok = actual != sentinel
                return ok, "≠ '/\\n/'"
            elif value == "2":
                ok = actual == sentinel
                return ok, "'/\\n/'"
            else:
                ok = actual == label
                return ok, label

        run_dropdown_filter_test(
            driver,
            wait,
            dropdown_id="fmFiltStatusPengamanan",
            cell_col_index=19,
            test_name=test_name,
            preprocess_actual=_pre,
            validator=_validator,
        )

    def test_TC_FLPM_017(self, test_name="TC_FLPM_017", column=17, line=1):
        print("test_" + test_name)
        tahun_buku_list = [
            "2015",
            "2017",
            "2008",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            tahun_buku_list,
            test_name,
            "fmTahunBuku",
            column_idx=column,
            line=line,
        )

    def test_TC_FLPM_018(self, test_name="TC_FLPM_018", column=9, line=1):
        print("test_" + test_name)
        driver = self.driver

        tahun_perolehans = [
            ("2008", "2013"),
            ("2017", "2019"),
            ("2024", "2025"),
        ]

        success_cases = 0
        failed = []

        cell_kode_xpath = f"./td[{column}]"

        for i, (start, end) in enumerate(tahun_perolehans, start=1):
            time.sleep(1)
            filter_range(
                driver, start, "fmTahunPerolehanAwal", end, "fmTahunPerolehanAkhir"
            )

            rows = get_table_rows(self.wait, driver)

            mismatches = []
            for idx_row, row in enumerate(rows, start=1):
                try:
                    td = row.find_element(By.XPATH, cell_kode_xpath)
                    raw = td.get_attribute("innerText") or ""
                    actual = get_actual_split(raw, line)

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

        cell_kode_xpath = "./td[16]"

        for i, (start, end) in enumerate(harga_perolehans, start=1):
            time.sleep(1)
            filter_range(
                driver, start, "fmHargaPerolehanAwal", end, "fmHargaPerolehanAkhir"
            )

            rows = get_table_rows(self.wait, driver)

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
                old_tbody = driver.find_element(By.CSS_SELECTOR, TBODY_CSS)
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
                EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS))
            )
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, DATA_ROW_XPATH)),
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

            rows = driver.find_elements(By.XPATH, DATA_ROW_XPATH)
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

    def test_TC_FLPM_021(self, test_name="TC_FLPM_021"):
        print("test_" + test_name)
        driver = self.driver

        per_pages = ["10", "25", "50", "100"]

        nodata_xpath = "//*[contains(translate(., 'TIDAK ADA DATA', 'tidak ada data'), 'tidak ada data') or contains(., 'No data')]"

        success_cases = 0
        failed = []

        for i, per_page in enumerate(per_pages, start=1):
            print(f"🔎 Kasus ke-{i}: jml per page = {per_page}")

            try:
                old_tbody = driver.find_element(By.CSS_SELECTOR, TBODY_CSS)
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
                EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS))
            )
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, DATA_ROW_XPATH)),
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

            rows = driver.find_elements(By.XPATH, DATA_ROW_XPATH)
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

        print_result(success_cases, len(per_pages), test_name=test_name)

        if failed:
            for f in failed:
                print(
                    f"- Gagal di kasus ke-{f['case']}: jumlah baris melebihi per page → Expected: '{f['exp']}', Actual: '{f['act']}'"
                )
            print(
                "========================================================================"
            )
        clear_readonly_input(self.driver, By.ID, "jmlperpage")

    def test_TC_FLPM_022(self):
        print("test_TC_FLPM_022")
        import re

        driver = self.driver

        price_cell_xpath = "./td[16]"
        total_row_xpath = "//table[@class='koptable']//tbody//tr[td//b[contains(normalize-space(),'Total per Halaman')]]"
        total_cell_xpath = (
            total_row_xpath
            + "/td[.//b[contains(normalize-space(),'Total per Halamatest_name)]]/following-sibling::td[1]"
        )
        nodata_xpath = (
            "//*[contains(translate(., 'TIDAK ADA DATA', 'tidak ada data'), 'tidak ada data') "
            "or contains(., 'No data')]"
        )

        def parse_rupiah(s: str) -> int:
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
            old_tbody = driver.find_element(By.CSS_SELECTOR, TBODY_CSS)
        except Exception:
            old_tbody = None

        try:
            if old_tbody:
                self.wait.until(EC.staleness_of(old_tbody))
        except TimeoutException:
            pass

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS)))
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, DATA_ROW_XPATH)),
                    EC.presence_of_element_located((By.XPATH, total_row_xpath)),
                    EC.presence_of_element_located((By.XPATH, nodata_xpath)),
                )
            )
        except TimeoutException:
            pass

        rows = driver.find_elements(By.XPATH, DATA_ROW_XPATH)

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
            f"Σ Computed: {computed_sum:,} | Actual Display: {displayed_total if displayed_total is not None else 'N/A'} ({total_text})"
        )

        if len(rows) == 0:
            test_pass = False
        else:
            test_pass = displayed_total is not None and computed_sum == displayed_total

        if test_pass:
            print_result(displayed_total, computed_sum, "TC_FLPM_022")
        else:
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

    def test_TC_FLPM_023(self):
        print("test_TC_FLPM_023")
        driver = self.driver
        form_input(driver, By.ID, "fmFiltNibar", TC_FLPM.nibar)
        time.sleep(1)
        Dropdown(driver, identifier="fmKondisiBarang", value="1")
        time.sleep(1)
        form_input(driver, By.ID, "fmKodeBarang", "1.3.2.02.01.01.005")
        time.sleep(1)
        form_input(driver, By.ID, "fmNamaBarang", "suv")
        time.sleep(1)
        form_input(driver, By.ID, "fmMerk", "Toyota")
        time.sleep(1)
        form_input(driver, By.ID, "fmNoPolisi", "A 662")
        time.sleep(1)
        form_input(driver, By.ID, "fmNoBPKB", "F 4032561")
        time.sleep(1)
        form_input(driver, By.ID, "fmNoMesin", "DBB5445")
        time.sleep(1)
        form_input(driver, By.ID, "fmNoRangka", "MHFE2CJ3C8K014559")
        time.sleep(1)
        form_input(driver, By.ID, "fmBahan", "campuran")
        time.sleep(1)
        form_input(driver, By.ID, "fmNoPabrik", "")
        time.sleep(1)
        form_input(driver, By.ID, "fmFiltKeterangan", "pengadaan")
        time.sleep(1)
        form_input(driver, By.ID, "fmFiltNamaPemakai", "luki")
        time.sleep(1)
        form_input(driver, By.ID, "fmFiltNoIdentitasPemakai", "12345678")
        time.sleep(1)
        form_input(driver, By.ID, "fmFiltNoBAST", "08/bast/2025")
        time.sleep(1)
        Dropdown(driver, identifier="fmFiltStatusPengamanan", value="1")
        time.sleep(1)
        form_input(driver, By.ID, "fmTahunBuku", "2008")
        time.sleep(1)
        tahun_perolehan = ["2008", "2010"]
        filter_range(
            driver,
            tahun_perolehan[0],
            "fmTahunPerolehanAwal",
            tahun_perolehan[1],
            "fmTahunPerolehanAkhir",
        )
        time.sleep(1)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS)))
        row = driver.find_elements(By.XPATH, DATA_ROW_XPATH)

        print_result(True, bool(row), test_name="TC_FLPM_023")
        clear_readonly_input(driver, By.ID, "fmFiltNibar")
        Dropdown(driver, identifier="fmKondisiBarang", value="__reset__")
        clear_readonly_input(driver, By.ID, "fmKodeBarang")
        clear_readonly_input(driver, By.ID, "fmNamaBarang")
        clear_readonly_input(driver, By.ID, "fmMerk")
        clear_readonly_input(driver, By.ID, "fmNoPolisi")
        clear_readonly_input(driver, By.ID, "fmNoBPKB")
        clear_readonly_input(driver, By.ID, "fmNoMesin")
        clear_readonly_input(driver, By.ID, "fmNoRangka")
        clear_readonly_input(driver, By.ID, "fmNoPabrik")
        clear_readonly_input(driver, By.ID, "fmBahan")
        clear_readonly_input(driver, By.ID, "fmFiltKeterangan")
        clear_readonly_input(driver, By.ID, "fmFiltNamaPemakai")
        clear_readonly_input(driver, By.ID, "fmFiltNoIdentitasPemakai")
        clear_readonly_input(driver, By.ID, "fmFiltNoBAST")
        Dropdown(driver, identifier="fmFiltStatusPengamanan", value="__reset__")
        clear_readonly_input(driver, By.ID, "fmTahunBuku")
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAwal")
        clear_readonly_input(driver, By.ID, "fmTahunPerolehanAkhir")

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


def validate_by_filter_form(
    driver,
    wait,
    values_to_check: list[str],
    test_name,
    filter_form,
    *,
    line: int = 1,
    column_idx: int | None = None,
    exact: bool = False,
    print_detail: bool = True,
):
    success = 0
    failed: list[tuple[int, str, str, str]] = []
    cell_xpath_tpl = "./td[{idx}]"

    for i, expected in enumerate(values_to_check, start=1):
        filter_pengamanan(driver, expected, filter_form)
        rows = get_table_rows(wait, driver)
        if not rows:
            print(f"ℹ️ Filter '{expected}': tidak ada data ditemukan.")
        else:
            print(f"✅ Filter '{expected}': {len(rows)} baris data ditemukan.")

        mismatches = []
        for r_idx, row in enumerate(rows, start=1):
            td = row.find_element(By.XPATH, cell_xpath_tpl.format(idx=column_idx))
            raw_text = td.get_attribute("innerText") or ""
            actual = get_actual_split(raw_text, line)
            if not is_found(actual, expected, exact):
                mismatches.append((r_idx, expected, actual, "mismatch nilai"))

        if mismatches:
            failed.extend(
                [(i, exp, act, reason) for (_, exp, act, reason) in mismatches]
            )
        else:
            success += 1

    if print_detail:
        total = len(values_to_check)
        print(f"{test_name}: {success}/{total} lolos")
        if failed:
            for idx_case, exp, act, reason in failed:
                print(
                    f"- Gagal pada item ke-{idx_case}: {reason} → Expected: '{exp}', Actual: '{act}'"
                )
            print("=" * 72)

    print_result(success, len(values_to_check), test_name)
    clear_readonly_input(driver, By.ID, filter_form)


def get_table_rows(wait, driver):
    try:
        old_tbody = driver.find_element(By.CSS_SELECTOR, TBODY_CSS)
    except Exception:
        old_tbody = None
    try:
        if old_tbody:
            wait.until(EC.staleness_of(old_tbody))
    except TimeoutException:
        pass
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS)))
    return driver.find_elements(By.XPATH, DATA_ROW_XPATH)


def get_actual_split(raw_text: str, line: int) -> str:
    all_lines = raw_text.splitlines()
    idx = line - 1
    if idx < 0 or idx >= len(all_lines):
        return ""
    value = all_lines[idx].strip()
    return value.rstrip("/")


def is_found(actual: str | None, name: str | None, exact: bool = False) -> bool:
    if not actual or not name:
        return False

    actual_clean = actual.strip().lower()
    name_clean = name.strip().lower()

    if exact:
        return actual_clean == name_clean
    else:
        return name_clean in actual_clean


def _iter_dropdown_options(driver, dropdown_locator):
    dropdown = Select(driver.find_element(*dropdown_locator))
    data = []
    for opt in dropdown.options:
        val = opt.get_attribute("value")
        if not val:
            continue
        data.append((val, (opt.text or "").strip()))
    return data


def _select_and_reload_table(driver, wait, dropdown_locator, value_to_select):
    Select(driver.find_element(*dropdown_locator)).select_by_value(value_to_select)
    try:
        old_tbody = driver.find_element(By.XPATH, DATA_ROW_XPATH)
    except Exception:
        old_tbody = None

    button(driver, By.ID, "btTampil")

    try:
        if old_tbody:
            wait.until(EC.staleness_of(old_tbody))
    except TimeoutException:
        pass

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, TBODY_CSS)))

    try:
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, DATA_ROW_XPATH)),
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


def run_dropdown_filter_test(
    driver,
    wait,
    *,
    dropdown_id: str,
    cell_col_index: int,
    test_name: str,
    preprocess_actual: Callable[[str], str] | None = None,
    validator: Callable[[str, str, str], tuple[bool, str]] | None = None,
):
    dropdown_locator = (By.ID, dropdown_id)
    options_data = _iter_dropdown_options(driver, dropdown_locator)

    failed = []
    test_pass = True

    for i, (value, label) in enumerate(options_data, start=1):
        print(f"🔎 Filter ke-{i}: {label} (value={value})")

        _select_and_reload_table(driver, wait, dropdown_locator, value)

        cells = driver.find_elements(By.XPATH, f"{DATA_ROW_XPATH}/td[{cell_col_index}]")

        if not cells:
            print(f"ℹ️ Tidak ada data untuk filter '{label}'.")
            continue

        for idx, el in enumerate(cells, start=1):
            raw = (el.text or "").strip()
            actual = preprocess_actual(raw) if preprocess_actual else raw

            if validator:
                ok, expected_desc = validator(value, label, actual)
            else:
                ok = actual == label
                expected_desc = label
            if not ok:
                failed.append({"row": idx, "exp": expected_desc, "act": actual})

    if failed:
        test_pass = False

    print_result(test_pass, True, test_name)

    if not test_pass:
        for f in failed:
            print(
                f"- Gagal di filter [{f['exp']}] baris ke-{f['row']} → Expected: '{f['exp']}', Actual: '{f['act']}'"
            )
        print("=" * 72)

    if dropdown_id:
        Dropdown(driver, identifier=dropdown_id, value="__reset__")


def filter_range(driver, start, locator_start, end, locator_end):
    form_input(driver, By.ID, locator_start, start)
    time.sleep(1)
    form_input(driver, By.ID, locator_end, end)
    time.sleep(1)
    button(driver, By.ID, "btTampil")


if __name__ == "__main__":
    unittest.main()
