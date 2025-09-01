import unittest
import os
from dotenv import load_dotenv
from components.button import button
from components.form_input import form_input
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from helpers.set_tanggal_buku import set_tgl_buku
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from components.checkbox import checkbox
from components.dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from datetime import datetime, timedelta


class TC_PNGK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_PNGK.nibar = os.getenv("nibar")
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananGedungTrans")

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()


    def test_TC_PNGK_001(self, isedit=False): 
        print("test_TC_PNGK_001")
        time.sleep(1)
        filter_pengamanan(self.driver, TC_PNGK.nibar)
        time.sleep(1)
        checkbox(self.driver, identifier=-1, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        try:
            href_button(self.driver, "javascript:pengamananGedungTrans.formPengembalian()")
            alert_expected = (
                "Penyebab Pengembalian belum diisi!" if isedit else "Penyebab Pengembalian belum diisi!"
            )
            time.sleep(2)
            save_get_alert(
                self.driver,
                expected=alert_expected,
                test_name="TC_PNGK_001"
                )
        except:
            print_result("Formt terbuka","form tidak terbuka","TC_PNGK_001")

    def test_TC_PNGK_002(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_002")
        value = "5"
        time.sleep(1)
        Dropdown(driver, identifier="fmpenyebab_pengembalian", value=value, by="id")
        time.sleep(1)
        
        if isedit:
            expected = "Penyebab Pengembalian lainnya belum diisi!"
        else:
            expected = "Penyebab Pengembalian Lainnya belum diisi!"

        actual = save_get_alert(
            driver,
            expected=expected,
            test_name="TC_PNGK_002")
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_003(self, isedit=False):
        driver = self.driver
        value = "1"
        time.sleep(1)
        Dropdown(driver, identifier="fmpenyebab_pengembalian", value=value, by="id")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Nomor BAST belum diisi!",
            test_name="TC_PNGK_003")
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_004(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_004")
        form_input(driver, By.ID, "fmno_bast", "08/bast/2025")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Tanggal BAST belum diisi!",
            test_name="TC_PNGK_004")
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_005(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_005")
        time.sleep(1)
        driver.find_element(By.ID, "fmtgl_bast").send_keys("05-05-2025")
        
        if isedit:
            expected = "Nama Penerima belum diisi!"
        else:
            expected = "Penerima belum dipilih!"
        
        actual = save_get_alert(
            driver,
            expected=expected,
            test_name="TC_PNGK_005")
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_006(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_006")
        button(driver, By.ID, "fmpenerima_nama_button")

        time.sleep(2)
        checkbox(self.driver, identifier=1, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        actual = save_get_alert(
            driver,
            expected="Pangkat Penerima belum diisi!",
            test_name="TC_PNGK_006")
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_007(self, isedit=False): 
        driver = self.driver
        print("test_TC_PNGK_007")
        form_input(driver, By.ID, "fmpenerima_pangkat", "4B")
        
        if isedit:
            expected = "Kondisi Pengembalian belum dipilih!"
        else:
            expected = "Kondisi Barang belum dipilih!"
        
        actual = save_get_alert(
            driver,
            expected=expected,
            test_name="TC_PNGK_007") 
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_008(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_008")
        value="1"
        Dropdown(driver, identifier="fmkondisi", value=value, by="id")
        actual = save_get_alert(
            driver,
            expected="Diinput Oleh belum diisi!",
            test_name="TC_PNGK_008"
        )
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_009(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_009")
        value="1"
        Dropdown(driver, identifier="fmdiinput_oleh", value=value, by="id")
        
        if isedit:
            expected = "Diinput Nama belum diisi!"
        else:
            expected = "Diinput Nama belum dipilih!"
        
        actual = save_get_alert(
            driver,
            expected=expected,
            test_name="TC_PNGK_009"
        )
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual
        
    def test_TC_PNGK_010(self, isedit= False):
        driver = self.driver
        print("test_TC_PNGK_010")

        button(driver, By.ID, "fmdiinput_nama_button")
        time.sleep(2)
        checkbox(self.driver, identifier=-1, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)      
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        dt = datetime.now()
        changed_dt = dt.replace(month=4, day=1).strftime("%d-%m-%Y")

        set_tgl_buku(self.driver, changed_dt)
        
        Tanggal_Pengamanan = dt.replace(month=5, day=1).strftime("%d-%m-%Y")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected=f"Tanggal Transaksi Pengembalian tidak lebih kecil dari Tanggal Pengamanan! ({Tanggal_Pengamanan})",
            test_name="TC_PNBK_011"
        )
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual
        
        time.sleep(2)

    def test_TC_PNGK_011(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGK_011")
                
        dt = datetime.now()
        changed_dt = dt.replace(month=5, day=4).strftime("%d-%m-%Y")

        set_tgl_buku(self.driver, changed_dt)
        Tanggal_BAST = dt.replace(month=5, day=5).strftime("%d-%m-%Y")
        
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected=f"Tanggal Transaksi Pengembalian tidak lebih kecil dari Tanggal Pengamanan! ({Tanggal_BAST})",
            test_name="TC_PNBK_011"
        )
        
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual
        
        time.sleep(2)
        
        #tersimpan
    def test_TC_PNGK_011(self):
        print("test_TC_PNGK_011")
                
        dt = datetime.now()
        changed_dt = dt.replace(month=5, day=6).strftime("%d-%m-%Y")

        set_tgl_buku(self.driver, changed_dt)
        button(self.driver, By.ID, "btSimpan")
        time.sleep(1)
        
        self.driver.get(f"{self.url}pages.php?Pg=pengembalianGedung")
        filter_pengamanan(self.driver, TC_PNGK.nibar)
        
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(5)

    def test_TC_PNGK_012(self, isedit=False):
        print("test_TC_PNGK_012")
        self.driver.get(f"{self.url}pages.php?Pg=pengamananGedungTrans")
        filter_pengamanan(self.driver, TC_PNGK.nibar)
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(1)
        checkbox(self.driver, identifier=-1, by="index", table_selector="table.koptable")
        href_button(self.driver, "javascript:pengamananGedungTrans.formPengembalian()")
        actual = save_get_alert(
            self.driver,
            expected=f"Sudah Pengembalian!",
            test_name="TC_PNGK_012",
            with_button=False
        )
        
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual

    def test_TC_PNGK_013(self, isedit=False):
        print("test_TC_PNGK_013")
        time.sleep(1)
        href_button(self.driver, "javascript:pengamananGedungTrans.Hapus()")
        
        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(1)

        actual = save_get_alert(
            self.driver,
            expected=f"Tidak bisa dibatalkan, sudah Pengembalian!",
            test_name="TC_PNGK_013",
            with_button=False
        )
        
        if isedit:
            return actual
        else:
            TC_PNGK.actual = actual
        

    # def test_ZZZ_998(self):
    #     self.driver.get(f"{self.url}pages.php?Pg=pengembalianGedung")
    #     self.driver.execute_script("document.body.style.zoom='80%'")
    #     time.sleep(1)
    #     checkbox(self.driver, identifier=-1, by="index", table_selector="table.koptable")
    #     time.sleep(1)
    #     self.driver.find_element(By.PARTIAL_LINK_TEXT, "Batal").click()
    #     time.sleep(1)

    #     alert = Alert(self.driver)
    #     alert_text = alert.text
    #     print(f"ℹ️ Alert muncul: {alert_text}")
    #     alert.accept()
    #     time.sleep(1)

    #     alert = Alert(self.driver)
    #     alert_text = alert.text
    #     print(f"ℹ️ Alert muncul: {alert_text}")
    #     alert.accept()
    #     time.sleep(1)


if __name__ == "__main__":
    unittest.main()
