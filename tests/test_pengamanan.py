import unittest
import os
from dotenv import load_dotenv
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from components.checkbox import checkbox
from components.dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
import time

from datetime import datetime, timedelta


class TestPengamanan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        print("✅ Login berhasil")
        time.sleep(3) # animasi dulu

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    #test_buka_modul_pengamanan(self): (ini di ubah karena unit testing di jalankan nya secara alphabetical order)
    #ini pembeda nya jadi dari angka terakhir 000,001,002,etc
    def test_TC_PNBR_000(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatan")
        page = ModulPengamananPage(self.driver)
        self.assertTrue(page.is_loaded(page_name="Pengamanan"), "❌ Modul Pengamanan gagal dimuat")
        time.sleep(2)
        self.driver.execute_script("document.body.style.zoom='70%'")

        
    def test_TC_PNBR_004(self):
        driver = self.driver
        print("test_TC_PNBR_004")
        
        driver.find_element(By.ID,"fmMerk").send_keys("TOYOTA INNOVA E")
        time.sleep(1)
        driver.find_element(By.ID,"btTampil").click()
        time.sleep(2)
        
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        driver.find_element(By.CLASS_NAME,"toolbar").click()
        time.sleep(1)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(1)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Pemakai belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
    def test_TC_PNBR_005(self):
        driver = self.driver
        print("test_TC_PNBR_005")
        time.sleep(3)
        driver.find_element(By.ID,"fmnama_pemakai_button").click()
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Status Pemakai belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        pass
    

    def test_TC_PNBR_006(self):
        driver = self.driver
        print("test_TC_PNBR_006")
        driver.find_element(By.CSS_SELECTOR,"#fmstatus_pemakai > option:nth-child(6)").click()
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Status Pemakai Lainnya belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        pass
    
    def test_TC_PNBR_007(self):
        driver = self.driver
        print("test_TC_PNBR_007")
        driver.find_element(By.CSS_SELECTOR,"#fmstatus_pemakai > option:nth-child(2)").click()
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Nomor Identitas Pemakai belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
    
    def test_TC_PNBR_008(self):
        driver = self.driver
        print("test_TC_PNBR_008")
        driver.find_element(By.ID,"fmno_ktp_pemakai").send_keys("3273145570007")
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Alamat Pemakai belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
    
    def test_TC_PNBR_009(self):
        driver = self.driver
        print("test_TC_PNBR_009")
        driver.find_element(By.ID,"fmalamat_pemakai").send_keys("Alamat Testing")
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Nomor BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
    
    
    def test_TC_PNBR_010(self):
        driver = self.driver
        print("test_TC_PNBR_010")
        driver.find_element(By.ID,"fmno_bast").send_keys("08/bast/2025")
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        #ui-datepicker-div > table > tbody > tr:nth-child(2) > td:nth-child(7) > a
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Tanggal BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
        
    
    def test_TC_PNBR_011(self):
        
        next_day = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        
        driver = self.driver
        print("test_TC_PNBR_011")
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys(next_day)
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Diinput Oleh belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
    
    def test_TC_PNBR_012(self):
        driver = self.driver
        print("test_TC_PNBR_012")
        driver.find_element(By.CSS_SELECTOR,"#fmdiinput_oleh > option:nth-child(2)").click()
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Diinput Nama belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
    # Skipped karena icon date image nya tidak dapat di tekan (skill issue sih kayak nya
    # def test_TC_PNBR_013(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_013")
        
        # User melakukan transaksi baru data P&M Pengamanan 47 tanggal transaski lebih kecil dari hari ini
        # Muncul alert tanggal transaksi tidak lebih kecil dari hari ini
        
    #     pass
    
    def test_TC_PNBR_014(self):
        driver = self.driver
        print("test_TC_PNBR_014")
        next_day = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        time.sleep(2)
        driver.find_element(By.ID,"fmdiinput_nama_button").click()
        time.sleep(2)
        checkbox(driver, identifier=2, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(1)
        
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        # Handle alert
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text.strip()
        print(f"ℹ️ Alert text: {alert_text}")
        
        expected_text = f"Tanggal Transaksi Pengamanan tidak lebih kecil dari Tanggal BAST! ({next_day})"
        self.assertIn(expected_text, alert_text, f"Alert text mismatch, got: {alert_text}")
        
        alert.accept()
    
    # Skipped karena icon date image nya tidak dapat di tekan (skill issue sih kayak nya)
    # def test_TC_PNBR_015(self): 
    #     driver = self.driver
    #     print("test_TC_PNBR_015")
        # User melakukan transaksi baru data P&M Pengamanan 47 tanggal transaski lebih kecil dari tgltransaksi terakhir
        # Muncul alert tanggal transaksi tidak lebih kecil dari tanggal transaksi terakhir
    #     pass
    
    def test_TC_PNBR_016(self):
        driver = self.driver
        day = (datetime.now() - timedelta(days=3)).strftime("%d-%m-%Y")
        print("test_TC_PNBR_016")
        
        time.sleep(2)
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").clear()
        driver.find_element(By.ID,"fmtgl_bast").send_keys(day)
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        time.sleep(2)
        driver.execute_script("document.body.style.zoom='70%'")
        time.sleep(3)
        pass
    
    def test_TC_PNBR_017(self):
        driver = self.driver
        print("test_TC_PNBR_017")
        driver.get(f"{self.url}index.php?Pg=05&SPg=05&jns=tetap")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(5)
        pass
    
    def test_TC_PNBR_018(self):
        driver = self.driver
        print("test_TC_PNBR_018")
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatan")
        time.sleep(3)
        driver.find_element(By.ID,"fmMerk").send_keys("TOYOTA INNOVA E")
        time.sleep(2)
        driver.find_element(By.ID,"btTampil").click()
        time.sleep(2)
        
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        driver.find_element(By.CLASS_NAME,"toolbar").click()
        
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Belum dilakukan pengembalian barang untuk pengguna/pemakai sebelumnya!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        
        pass
    
    def test_ZZZ_998(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(3)
        self.driver.find_element(By.ID,"pengamananPeralatanTrans_cb0").click()
        time.sleep(3)
        self.driver.find_element(By.PARTIAL_LINK_TEXT,"Batal").click()
        time.sleep(3)
        
        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(3)
        
        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(1)
            
    def test_ZZZ_999(self):
        logout(self.driver)
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
