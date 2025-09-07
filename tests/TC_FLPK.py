import re
from datetime import datetime
import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from components.button import button
from components.dropdown import Dropdown
from components.form_input import form_input
from helpers.clear_readonly_input import clear_readonly_input
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from selenium.webdriver.support.ui import Select, WebDriverWait
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time

from tests.TC_FLPM import (
    DATA_ROW_XPATH,
    TBODY_CSS,
    TC_FLPM,
    run_dropdown_filter_test,
    validate_by_filter_form,
)


class TC_FLPK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_FLPK.nibar = os.getenv("nibar")
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananPeralatanTrans")
        time.sleep(1)
        cls.wait = WebDriverWait(driver, 5)
        cls.tc_flpm = TC_FLPM()
        cls.tc_flpm.driver = cls.driver
        cls.tc_flpm.wait = cls.wait

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

    def test_TC_FLPK_002(self):
        print("test_TC_FLPK_002")
        self.tc_flpm.test_TC_FLPM_001("test_TC_FLPK_002")

    def test_TC_FLPK_003(self):
        self.tc_flpm.test_TC_FLPM_002("test_TC_FLPK_003", col="6")

    def test_TC_FLPK_004(self):
        self.tc_flpm.test_TC_FLPM_003("test_TC_FLPK_004")

    def test_TC_FLPK_005(self):
        self.tc_flpm.test_TC_FLPM_004("test_TC_FLPK_005")

    def test_TC_FLPK_006(self):
        self.tc_flpm.test_TC_FLPM_005("test_TC_FLPK_006", line=2)

    def test_TC_FLPK_007(self):
        self.tc_flpm.test_TC_FLPM_006("test_TC_FLPK_007", column=6, line=3)

    def test_TC_FLPK_012(self):
        self.tc_flpm.test_TC_FLPM_013("test_TC_FLPK_012", column=8)

    def test_TC_FLPK_014(self):
        test_name = "TC_FLPK_014"
        print("test_" + test_name)
        jabatan_list = [
            "Kepala UPTD BPTPHP",
            "Kepala Bidang PKTL",
            "d",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            jabatan_list,
            test_name,
            "fmFiltJabatanPemakai",
            column_idx=10,
        )

    def test_TC_FLPK_015(self):
        test_name = "TC_FLPK_015"
        print("test_" + test_name)
        alamat_list = [
            "Alamat testing",
            "tes",
            "d",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            alamat_list,
            test_name,
            "fmFiltAlamatPemakai",
            column_idx=12,
        )

    def test_TC_FLPK_016(self):
        self.tc_flpm.test_TC_FLPM_014("test_TC_FLPK_016", column=11, line=1)

    def test_TC_FLPK_017(self):
        self.tc_flpm.test_TC_FLPM_015("test_TC_FLPK_017", column=13, line=1)

    def test_TC_FLPK_018(self):
        test_name = "TC_FLPK_018"
        print("test_" + test_name)
        tahun_list = [
            "2025",
            "2023",
            "2022",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            tahun_list,
            test_name,
            "fmFiltTahunBAST",
            column_idx=13,
        )

    def test_TC_FLPK_019(self):
        test_name = "TC_FLPK_019"
        print("test_" + test_name)
        ket_list = [
            "tes",
            "apa",
            "coba",
        ]

        validate_by_filter_form(
            self.driver,
            self.wait,
            ket_list,
            test_name,
            "fmFiltKetPemakaian",
            column_idx=17,
        )

    def test_TC_FLPK_020(self):
        driver = self.driver
        wait = self.wait

        def _pre(actual_raw: str) -> str:
            return actual_raw.strip()

        def _validator(value: str, label: str, actual: str) -> tuple[bool, str]:
            if value == "1":
                ok = actual == ""
                return ok, "≠ ''"
            elif value == "2":
                ok = True
                return ok, actual
            else:
                ok = actual == label
                return ok, label

        run_dropdown_filter_test(
            driver,
            wait,
            dropdown_id="fmFiltStatusPengembalian",
            cell_col_index=18,
            test_name="TC_FLPM_020",
            preprocess_actual=_pre,
            validator=_validator,
        )

    def test_TC_FLPK_021(self):
        self.tc_flpm.test_TC_FLPM_017("TC_FLPK_021", 6, 5)

    def test_TC_FLPK_022(self):
        self.tc_flpm.test_TC_FLPM_018("test_TC_FLPK_022", column=6, line=4)

    def test_TC_FLPK_024(self):
        print("test_TC_FLPK_024")

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

        def _parse_date_or_year(text: str):
            text = (text or "").strip()
            for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
                try:
                    return datetime.strptime(
                        text, fmt
                    ), text  # kembalikan datetime & raw
                except ValueError:
                    pass
            m = re.search(r"\b(?:19|20)\d{2}\b", text)
            if m:
                return datetime(int(m.group(0)), 1, 1), text
            return None, text  # gagal total

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
                        td = row.find_element(By.XPATH, "./td[14]")
                        raw = (td.get_attribute("innerText") or "").strip()
                    except NoSuchElementException:
                        continue
                    dt, raw_text = _parse_date_or_year(raw)
                    values.append((idx_row, dt, raw_text))

                for j in range(1, len(values)):
                    _, prev_dt, _ = values[j - 1]
                    cur_idx, cur_dt, cur_raw = values[j]

                    if cur_dt is None or prev_dt is None or cur_dt < prev_dt:
                        exp_str = f">= {prev_dt.strftime('%d-%m-%Y') if isinstance(prev_dt, datetime) else 'DD-MM-YYYY'}"
                        failed.append(
                            {
                                "row": cur_idx,
                                "exp": exp_str,
                                "act": cur_raw,
                            }
                        )

            elif value == "2":
                values = []
                for idx_row, row in enumerate(rows, start=1):
                    try:
                        td = row.find_element(By.XPATH, "./td[17]")
                        raw = (td.get_attribute("innerText") or "").strip()
                    except NoSuchElementException:
                        continue
                    if raw == "":
                        continue

                    dt, raw_text = _parse_date_or_year(raw)
                    values.append((idx_row, dt, raw_text))

                for j in range(1, len(values)):
                    _, prev_dt, _ = values[j - 1]
                    cur_idx, cur_dt, cur_raw = values[j]

                    if cur_dt is None or prev_dt is None or cur_dt < prev_dt:
                        exp_str = f">= {prev_dt.strftime('%d-%m-%Y') if isinstance(prev_dt, datetime) else 'DD-MM-YYYY'}"
                        failed.append(
                            {
                                "row": cur_idx,
                                "exp": exp_str,
                                "act": cur_raw,
                            }
                        )
            elif value == "3":
                values = []
                for idx_row, row in enumerate(rows, start=1):
                    try:
                        td = row.find_element(By.XPATH, "./td[4]")
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

    def test_TC_FLPK_025(self):
        self.tc_flpm.test_TC_FLPM_021("TC_FLPK_025")

    def test_TC_FLPK_027(self):
        self.test_TC_FLPK_002()
        self.test_TC_FLPK_003()
        self.test_TC_FLPK_004()
        self.test_TC_FLPK_005()
        self.test_TC_FLPK_006()
        self.test_TC_FLPK_007()
        self.test_TC_FLPK_012()
        self.test_TC_FLPK_014()
        self.test_TC_FLPK_015()
        self.test_TC_FLPK_016()
        self.test_TC_FLPK_017()
        self.test_TC_FLPK_018()
        self.test_TC_FLPK_019()
        self.test_TC_FLPK_020()
        self.test_TC_FLPK_021()
        self.test_TC_FLPK_022()
        self.test_TC_FLPK_024()
        self.test_TC_FLPK_025()


if __name__ == "__main__":
    unittest.main()
