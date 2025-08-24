import unittest
import os
from dotenv import load_dotenv
from components.button import button
from components.form_input import form_input
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_pengamanan
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from components.checkbox import checkbox
from components.dropdown import Dropdown
from helpers.set_tanggal_buku import set_tgl_buku
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from datetime import datetime, timedelta


class TC_PNBK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_PNBK.nibar = os.getenv("nibar")
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananPeralatanTrans")

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()
        
    def test_TC_PNBK_001(self ,isedit=False):
        print("test_TC_PNBK_001")
        filter_pengamanan(self.driver, TC_PNBK.nibar)
        time.sleep(1)
        checkbox(self.driver, identifier=2, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        href_button(self.driver, "javascript:pengamananPeralatanTrans.formPengembalian()")
        
        alert_expected = (
            "Penyebab Pengembalian belum diisi!" if isedit else "Penyebab Pengembalian belum diisi!" 
        )
        time.sleep(1)
        save_get_alert(
            self.driver,
            expected=alert_expected,
            test_name="TC_PNBK_001")
    
    def test_TC_PNBK_002(self):
        driver = self.driver
        print("test_TC_PNBK_002")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,"#fmpenyebab_pengembalian > option:nth-child(6)").click()
        time.sleep(1)
        save_get_alert(
            self.driver,
            expected="Penyebab Pengembalian Lainnya belum diisi!",
            test_name="TC_PNBK_002"
            )
        time.sleep(1)
    
    def test_TC_PNBK_003(self):
        driver = self.driver
        print("test_TC_PNBK_003")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,"#fmpenyebab_pengembalian > option:nth-child(2)").click()
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Nomor BAST belum diisi!",
            test_name="TC_PNBK_003")
        time.sleep(1)
        
    def test_TC_PNBK_004(self):
        driver = self.driver
        print("test_TC_PNBK_004")
        time.sleep(1)
        form_input(driver, By.ID, "fmno_bast", "08/bast/2025")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Tanggal BAST belum diisi!",
            test_name="TC_PNBK_004")
        
    def test_TC_PNBK_005(self):
        driver = self.driver
        print("test_TC_PNBK_005")
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys("testing non tgl")
        time.sleep(1)
        save_get_alert(
            driver,
            expected="Tanggal BAST belum diisi!",
            test_name="TC_PNBK_005")        
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").clear()
        time.sleep(1)
        
    def test_TC_PNBK_006(self):
        driver = self.driver
        print("test_TC_PNBK_006")
        
        dt = datetime.now()
        tgl_bast = dt.replace(month=5, day=1).strftime("%d-%m-%Y")
    
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys(tgl_bast)
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,
            expected="Penerima belum dipilih!",
            test_name="TC_PNBK_006")     
        
        time.sleep(2)
        
    def test_TC_PNBK_007(self):
        driver = self.driver
        print("test_TC_PNBK_007")
        
        button(driver, By.ID, "fmpenerima_nama_button")
        
        time.sleep(2)
        checkbox(self.driver, identifier=1, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,
            expected="Pangkat Penerima belum diisi!",
            test_name="TC_PNBK_007")     
        
        time.sleep(1)
        
    def test_TC_PNBK_008(self):
        driver = self.driver
        print("test_TC_PNBK_008")
        
        self.driver.find_element(By.ID,"fmpenerima_pangkat").send_keys("4B")
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,
            expected="Kondisi Barang belum dipilih!",
            test_name="TC_PNBK_008") 
        
        time.sleep(2)
        
    def test_TC_PNBK_009(self):
        driver = self.driver
        print("test_TC_PNBK_009")
        
        driver.find_element(By.CSS_SELECTOR,"#fmkondisi > option:nth-child(2)").click()
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,
            expected="Diinput Oleh belum diisi!",
            test_name="TC_PNBK_009"
            ) 
        
        time.sleep(2)
        
    def test_TC_PNBK_010(self):
        driver = self.driver
        print("test_TC_PNBK_010")
        
        driver.find_element(By.CSS_SELECTOR,"#fmdiinput_oleh > option:nth-child(2)").click()
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,  
            expected="Diinput Nama belum dipilih!", 
            test_name="TC_PNBK_010"
            ) 
        
        time.sleep(2)
        
    def test_TC_PNBK_011(self):
        driver = self.driver
        print("test_TC_PNBK_011")
        
        button(driver, By.ID, "fmdiinput_nama_button")
        time.sleep(2)
        checkbox(self.driver, identifier=2, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)      
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        dt = datetime.now()
        changed_dt = dt.replace(month=4, day=1).strftime("%d-%m-%Y")

        set_tgl_buku(self.driver, changed_dt)
        Tanggal_Pengamanan = dt.replace(month=5, day=2).strftime("%d-%m-%Y")
        
        time.sleep(1)
        save_get_alert(
            driver,
            expected=f"Tanggal Transaksi Pengembalian tidak lebih kecil dari Tanggal Pengamanan! ({Tanggal_Pengamanan})",
            test_name="TC_PNBK_011"
        )
        
        time.sleep(2)
        
    def test_TC_PNBK_012(self):
        driver = self.driver
        print("test_TC_PNBK_012")
        
        dt = datetime.now()
        changed_dt = dt.replace(month=5, day=2).strftime("%d-%m-%Y")
        set_tgl_buku(self.driver, changed_dt)
        
        Tanggal_BAST_Pemakaian = dt.replace(month=5, day=2).strftime("%d-%m-%Y")
        
        time.sleep(1)
        save_get_alert(
            driver,
            expected=f"Tanggal BAST tidak boleh lebih kecil dari tanggal BAST pemakaian! ({Tanggal_BAST_Pemakaian})",
            test_name="TC_PNBK_012"
        )
        
    def test_TC_PNBK_013(self):
        driver = self.driver
        print("test_TC_PNBK_013")

        dt = datetime.now()
        tgl_bast = dt.replace(month=5, day=3).strftime("%d-%m-%Y")

        driver.find_element(By.ID,"fmtgl_bast").clear()
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys(tgl_bast)
        
        time.sleep(1)
        save_get_alert(
            driver,
            expected=f"Tanggal Transaksi Pengembalian tidak lebih kecil dari Tanggal BAST! ({tgl_bast})",
            test_name="TC_PNBK_013"
        )
        
        
    def test_TC_PNBK_014(self):
        print("test_TC_PNBK_014")
        
        dt = datetime.now()
        changed_dt = dt.replace(month=12, day=30).strftime("%d-%m-%Y")
        set_tgl_buku(self.driver, changed_dt)
        
        time.sleep(2)
        
        # save_get_alert(
        #     self.driver,
        #     expected=f"tanggal transaksi tidak lebih besar dari hari ini",
        #     "TC_PNBK_014"
        # )
        
    def test_TC_PNBK_015(self):
        driver = self.driver
        print("test_TC_PNBK_015")
        
        try:
            driver.find_element(By.ID, "fmtgl_bast")

            dt = datetime.now()
            changed_dt = dt.replace(month=5, day=3).strftime("%d-%m-%Y")
            set_tgl_buku(self.driver, changed_dt)
            
            dt = datetime.now()
            tgl_bast = dt.replace(month=1, day=1).strftime("%d-%m-%Y")
            Tanggal_BAST_Pemakaian = dt.replace(month=5, day=2).strftime("%d-%m-%Y")

            driver.find_element(By.ID,"fmtgl_bast").clear()
            driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
            time.sleep(1)
            driver.find_element(By.ID,"fmtgl_bast").send_keys(tgl_bast)
            
            time.sleep(1)
            save_get_alert(
                driver,
                expected=f"Tanggal BAST tidak boleh lebih kecil dari tanggal BAST pemakaian! ({Tanggal_BAST_Pemakaian})",
                test_name="TC_PNBK_015"
            )
            time.sleep(1)
            
        except NoSuchElementException:
            print_result("Data Tersimpan", "Muncul Alert Sebelum nya", test_name="TC_PNBK_015")
        
    def test_TC_PNBK_016(self): # tersimpan
        driver = self.driver
        print("test_TC_PNBK_016")
        try:
            driver.find_element(By.ID, "fmtgl_bast")
            dt = datetime.now()
            
            tgl_bast = dt.replace(month=5, day=3).strftime("%d-%m-%Y")
            driver.find_element(By.ID,"fmtgl_bast").clear()
            driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
            time.sleep(1)
            driver.find_element(By.ID,"fmtgl_bast").send_keys(tgl_bast)

            changed_dt = dt.replace(month=5, day=3).strftime("%d-%m-%Y")
            set_tgl_buku(self.driver, changed_dt)

            time.sleep(1)
            driver.find_element(By.ID, "btSimpan").click()
            time.sleep(1)

            driver.get(f"{self.url}pages.php?Pg=pengembalianPeralatan")
            filter_pengamanan(self.driver, TC_PNBK.nibar)
            time.sleep(1)

            self.driver.execute_script("document.body.style.zoom='80%'")
            time.sleep(5)

        except NoSuchElementException:
            print_result("Data Tersimpan", "Muncul Alert Sebelum nya", test_name="TC_PNBK_016")    
            
    def test_TC_PNBK_017(self):
        driver = self.driver
        print("test_TC_PNBK_017")
        driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        time.sleep(1)
        checkbox(self.driver, identifier=2, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        href_button(self.driver, "javascript:pengamananPeralatanTrans.formPengembalian()")
        
        time.sleep(1)
        #tidak di pakai save_get _alert karena di fungsi itu mencari btnsimpan terlebih dahulu 
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(
            alert_text,"Sudah Pengembalian!",
            f"Teks alert tidak sesuai, dapat: {alert_text}",
        )
        print_result(
            alert.text,
            "Sudah Pengembalian!",
            "TC_PNBK_017")
        alert.accept()
        
    
    def test_ZZZ_998(self):
        print("reset")
        time.sleep(1)
        self.driver.get(f"{self.url}pages.php?Pg=pengembalianPeralatan")
        filter_pengamanan(self.driver, TC_PNBK.nibar)
        time.sleep(1)
        checkbox(self.driver, identifier=2, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(self.driver, "javascript:pengembalianPeralatan.Hapus()")
        time.sleep(1)
        
        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(2)
        
        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(1)    
            


if __name__ == "__main__":
    unittest.main()
