from datetime import date, datetime
import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from components.button import button
from components.dropdown import Dropdown
from components.form_input import form_input
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.PM.save_get_alert import save_get_alert
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar_pembukuan
from helpers.logout_helper import logout
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time
import calendar
from zoneinfo import ZoneInfo


class TC_PNPT(unittest.TestCase):
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
        TC_PNPT.nibar = os.getenv("nibar")
        time.sleep(3)
        driver.get(f"{cls.url}index.php?Pg=05&SPg=03&jns=tetap")
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()
        
        # cls.driver.quit()

    def setUp(self):
        driver = self.driver

        if self._testMethodName != "test_TC_PNPT_001":
            filter_nibar_pembukuan(self.driver, self.__class__.nibar)
            time.sleep(1)
            checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
            time.sleep(1)

            actions = {
                "test_TC_PNPT_012": "javascript:Reclass.reClass()",
                "test_TC_PNPT_013": "javascript:MutasiBaru_ins.mutasibaru()",
                "test_TC_PNPT_015": "javascript:pecah.Baru()",
                "test_TC_PNPT_016": "javascript:reklasifikasi.Baru()",
                "test_TC_PNPT_017": "javascript:pemanfaatanV2.formMulti()",
                "test_TC_PNPT_018": "javascript:pemindahtanganan_ins.pemindahtangananbaru()()",
                "test_TC_PNPT_019": "javascript:pemusnahan_ins.pemusnahanbaru()",
                "test_TC_PNPT_020": "javascript:kapitalisasi_ins.kapitalisasibaru()",
                "test_TC_PNPT_021": "javascript:kondisi_ins.kondisibaru()",
                "test_TC_PNPT_022": "javascript:reclass_persediaan.Baru()",
                "test_TC_PNPT_023": "javascript:updatebarang.showFormUbahKondisi('cidBI[]',1)",
                "test_TC_PNPT_024": "javascript:AsetLainLain.fmReklas('cidBI[]',1)",
            }

            if self._testMethodName in actions:
                href_button(self.driver, actions[self._testMethodName])
                if self._testMethodName not in {
                    "test_TC_PNPT_012",
                    "test_TC_PNPT_015",
                    "test_TC_PNPT_016",
                    "test_TC_PNPT_017",
                    "test_TC_PNPT_023",
                    "test_TC_PNPT_024",
                }:
                    alert = self.wait.until(EC.alert_is_present())
                    time.sleep(1)
                    alert.accept()
                    time.sleep(1)
            else:
                href_button(self.driver, "javascript:updatebarang.formUpdate()")
                time.sleep(1)
                
            handles = self.driver.window_handles
            if len(handles) > 1:
                self.driver.switch_to.window(handles[-1])

    def tearDown(self):
        d = getattr(self, "driver", None)
        if not d or not getattr(d, "session_id", None):
            return

        try:
            handles = d.window_handles
            if not handles:
                return

            if len(handles) > 1:
                current = d.current_window_handle
                target = next((h for h in reversed(handles) if h != current), None)
                d.close()
                if target:
                    d.switch_to.window(target)
            else:
                pass
        except Exception as e:
            print(f"[⚠️] Gagal menutup tab atau berpindah: {e}")

    def test_TC_PNPT_001(self):
        driver = self.driver
        filter_nibar_pembukuan(self.driver, TC_PNPT.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:prosesEdit()")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("test_TC_PNPT_001")
        driver = self.driver
        element = driver.find_element(By.ID, "fmKET_KIB_B")
        current_value = element.get_attribute("value") or ""
        new_value = current_value + " untuk testing"
        form_input(driver, By.ID, "fmKET_KIB_B", new_value)
        time.sleep(1)
        save_get_alert(driver, "Data telah di simpan", "TC_PNPT_001", "btsave")
        driver.switch_to.window(driver.window_handles[0])

    def test_TC_PNPT_002(self):
        print("test_TC_PNPT_002")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "1")
        time.sleep(1)
        form_input(driver, By.ID, "hrg_baru", "150000000")
        time.sleep(1)
        form_input(driver, By.ID, "ket_koreksi", "test")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        self.alert_helper("TC_PNPT_002")

    def test_TC_PNPT_003(self):
        print("test_TC_PNPT_003")
        driver = self.driver
        time.sleep(2)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "2")
        time.sleep(1)

        # biar lebih robust
        kondisi_text = driver.find_element(
            By.CSS_SELECTOR,
            "#areakondisi > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(3)",
        ).text.strip()

        if kondisi_text == "Baik":
            Dropdown(driver, "kondisi_baru", "2")
        else:
            Dropdown(driver, "kondisi_baru", "1")

        time.sleep(1)
        form_input(driver, By.ID, "ket_kondisi", "penurunan nilai barang")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT__003",
            with_button=False,
        )

    def test_TC_PNPT_004(self):
        print("test_TC_PNPT_004")
        driver = self.driver
        time.sleep(2)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "3")
        time.sleep(1)
        form_input(driver, By.ID, "ketKapitalisasi", "penurunan nilai barang")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT",
            with_button=False,
        )

    def test_TC_PNPT_005(self):
        print("test_TC_PNPT_005")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "5")
        time.sleep(1)
        button(driver, By.XPATH, "//input[@value='CARI BARANG']")
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "5241695")  # akun sulthan
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_005",
            with_button=False,
        )
        
    def test_TC_PNPT_006(self):
        print("test_TC_PNPT_006")
        driver = self.driver
        time.sleep(2)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "6")
        time.sleep(1)
        button(
            driver,
            By.CSS_SELECTOR,
            "#areagabung > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]:nth-child(2)",
        )
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "16815")  # akun sulthan
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing penggabungan")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected=f"NIBAR {TC_PNPT.nibar} masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_006",
            with_button=False,
        )

    def test_TC_PNPT_007(self):
        print("test_TC_PNPT_007")
        driver = self.driver
        time.sleep(2)
        form_input(driver, By.ID, "no_bast", "07/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "8")
        time.sleep(1)
        button(driver, By.ID, "caribarang")
        time.sleep(1)
        form_input(driver, By.ID, "fmBARANG", "SUV")
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_updtKdBrg", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_007",
            with_button=False,
        )

    def test_TC_PNPT_008(self):
        print("test_TC_PNPT_008")
        driver = self.driver
        time.sleep(2)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "9")
        time.sleep(1)
        form_input(driver, By.ID, "ket_KoreksiKurang", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_008",
            with_button=False,
        )

    @unittest.skip("untuk testing")
    def test_TC_PNPT_009(self):
        print("test_TC_PNPT_009")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "6")
        time.sleep(1)
        button(
            driver,
            By.CSS_SELECTOR,
            "#areagabung > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]:nth-child(2)",
        )
        time.sleep(1)
        form_input(
            driver, By.ID, "IDBARANG", "16814"
        )  # Karena yang induk nya yang di jadikan target ini jadi terbalik env nibar = 16815(yang pengamanan)
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing penggabungan")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected=f"Data berhasil di simpan !",
            test_name="TC_PNPT_009",
            with_button=False,
        )

    @unittest.skip("untuk testing")
    def test_TC_PNPT_010(self):
        print("test_TC_PNPT_010")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "5")
        time.sleep(1)
        button(driver, By.XPATH, "//input[@value='CARI BARANG']")
        time.sleep(1)
        form_input(
            driver, By.ID, "IDBARANG", "16814"
        )  # akun sulthan mini bus dengan env nibar 24959000 ( sama kasus nya dengan 009, 16814 adalah induk nya jadi yang terhapus adalah 24959000)
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected="Data berhasil di simpan !",
            test_name="TC_PNPT_010",
            with_button=False,
        )

    def test_TC_PNPT_011(self):
        print("test_TC_PNPT_011")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "7")
        time.sleep(1)
        form_input(driver, By.ID, "fmHARGA_HAPUS", "2000000")
        time.sleep(1)
        form_input(driver, By.ID, "fmKET", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Data berhasil di simpan",
            test_name="TC_PNPT_011",
            with_button=False,
        )

    def test_TC_PNPT_012(self):
        print("test_TC_PNPT_012")
        driver = self.driver
        time.sleep(1)
        button(driver, By.ID, "caribarang")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_012",
            with_button=False,
        )

    @unittest.skip("untuk testing")
    def test_TC_PNPT_013(self):
        tc = "TC_PNPT_013"
        print(f"test_{tc}")
        driver = self.driver
        Dropdown(driver, "fmSKPDBidang2", "25")
        time.sleep(1)
        Dropdown(driver, "fmSKPDskpd2", "01")
        time.sleep(1)
        Dropdown(driver, "fmSKPDUnit2", "0001")
        time.sleep(1)
        Dropdown(driver, "fmSKPDSubUnit2", "001")
        time.sleep(1)
        Dropdown(driver, "no_bast", "08/BAST")
        time.sleep(1)
        form_input(driver, By.ID, "ket", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        alert = self.wait.until(EC.alert_is_present())
        time.sleep(1)
        alert.accept()
        time.sleep(1)
        self.errmsg_helper(tc)

    def test_TC_PNPT_015(self):
        tc = "TC_PNPT_015"
        print(f"test_{tc}")
        self.alert_helper(tc)

    def test_TC_PNPT_016(self):
        driver = self.driver
        tc = "TC_PNPT_016"
        form_input(driver, By.ID, "fmnama_dok", "tes")
        form_input(driver, By.ID, "fmnomor", "tes")
        print(f"test_{tc}")
        button(driver, By.XPATH, "//input[@type='button' and @value='Simpan']")
        self.alert_helper(tc)

    def test_TC_PNPT_017(self):
        driver = self.driver
        tc = "TC_PNPT_017"
        print(f"test_{tc}")
        today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
        tgl_str = f"{today.day:02d}"  # contoh: "07"
        bln_str = f"{today.month:02d}"  # contoh: "09"
        thn_str = str(today.year)  # contoh: "2025"

        end_dt = add_one_month_safe(today)
        end_tgl_str = f"{end_dt.day:02d}"
        end_bln_str = f"{end_dt.month:02d}"
        end_thn_str = str(end_dt.year)

        Dropdown(driver, "fmTANGGALPEMANFAATAN_tgl", tgl_str)
        time.sleep(1)
        Dropdown(driver, "fmTANGGALPEMANFAATAN_bln", bln_str)
        time.sleep(1)

        Dropdown(driver, "fmBENTUKPEMANFAATAN", "1")
        time.sleep(1)

        Dropdown(driver, "fmSURATTANGGAL_tgl", tgl_str)
        time.sleep(1)
        Dropdown(driver, "fmSURATTANGGAL_bln", bln_str)
        time.sleep(1)
        Dropdown(driver, "fmSURATTANGGAL_thn", thn_str)
        time.sleep(1)

        Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_tgl", end_tgl_str)
        time.sleep(1)
        Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
        Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
        time.sleep(1)
        form_input(driver, By.ID, "fmTANGGALPEMANFAATAN_akhir_thn", end_thn_str)
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        self.alert_helper(tc)

    def test_TC_PNPT_018(self):
        driver = self.driver
        tc = "TC_PNPT_018"
        print(f"test_{tc}")
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        Dropdown(driver, "fmBENTUKPEMINDAHTANGANAN", "1")
        time.sleep(1)
        href_button(driver, "javascript:pemindahtanganan_ins.Simpan()")
        self.errmsg_helper(tc)

    def test_TC_PNPT_019(self):
        driver = self.driver
        tc = "TC_PNPT_019"
        print(f"test_{tc}")
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        form_input(driver, By.ID, "cr_pemusnahan", "tes")
        time.sleep(1)
        href_button(driver, "javascript:pemusnahan_ins.Simpan3()")
        self.errmsg_helper(tc)

    def test_TC_PNPT_020(self):
        driver = self.driver
        tc = "TC_PNPT_020"
        print(f"test_{tc}")
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        href_button(driver, "javascript:kapitalisasi_ins.Simpan()")
        self.errmsg_helper(tc)

    def test_TC_PNPT_021(self):
        driver = self.driver
        tc = "TC_PNPT_021"
        print(f"test_{tc}")
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        href_button(driver, "javascript:kondisi_ins.Simpan()")
        self.errmsg_helper(tc)

    def test_TC_PNPT_022(self):
        driver = self.driver
        tc = "TC_PNPT_022"
        print(f"test_{tc}")
        form_input(driver, By.ID, "no_sk", "tes")
        time.sleep(1)
        href_button(driver, "javascript:reclass_persediaan.Simpan()")
        self.errmsg_helper(tc)

    def test_TC_PNPT_023(self):
        driver = self.driver
        tc = "TC_PNPT_023"
        print(f"test_{tc}")
        form_input(driver, By.ID, "fnoba", "tes")
        time.sleep(1)
        Dropdown(driver, "fkondisi", "2")
        time.sleep(1)
        button(driver, By.ID, "btProses")
        self.alert_helper(tc)

    def test_TC_PNPT_024(self):
        driver = self.driver
        tc = "TC_PNPT_024"
        print(f"test_{tc}")
        form_input(driver, By.ID, "fnoba", "tes")
        time.sleep(1)
        Dropdown(driver, "fkategori", "2")
        time.sleep(1)
        button(driver, By.ID, "btProses")
        self.alert_helper(tc)
        alert = self.wait.until(EC.alert_is_present())
        if alert:
            alert.accept()

    def alert_helper(
        self,
        testCase,
        expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!",
    ):
        try:
            alert = self.wait.until(EC.alert_is_present())
            if alert:
                actual = alert.text.strip() == expected
                print_result(actual, True, testCase)
                alert.accept()
            else:
                print_result(False, True, testCase)
        except TimeoutException:
            print_result(False, True, testCase)

    def errmsg_helper(self, testCase, errMsgId="errmsg"):
        time.sleep(5)
        try:
            textarea = self.wait.until(
                EC.presence_of_element_located((By.ID, errMsgId))
            )
            value = textarea.get_attribute("value") or ""
            actual = value.strip() != ""

            print_result(actual, True, testCase)
        except TimeoutException:
            self.fail("[❌] Textarea dengan id 'errmsg' tidak ditemukan dalam 10 detik")


def add_one_month_safe(dt: date) -> date:
    y, m = dt.year, dt.month + 1
    if m == 13:
        y, m = y + 1, 1
    last_day_next = calendar.monthrange(y, m)[1]
    d = min(dt.day, last_day_next)
    return date(y, m, d)


if __name__ == "__main__":
    unittest.main()
