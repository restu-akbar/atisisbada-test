import unittest
import os
from dotenv import load_dotenv
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from components.checkbox import checkbox
from components.href_button import href_button
from components.button import button

from components.dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
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
    def test_TC_PNBK_000(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")

        time.sleep(2)
        self.driver.execute_script("document.body.style.zoom='80%'")

        
    def test_TC_PNBK_001(self):
        driver = self.driver
        print("test_TC_PNBR_001")
        driver.find_element(By.ID,"fmNamaBarang").send_keys("Mini Bus")
        time.sleep(1)
        driver.find_element(By.ID,"btTampil").click()
        
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        self.driver.find_element(By.PARTIAL_LINK_TEXT,"Kembali").click()
        button(driver, By.ID, "btSimpan")
        time.sleep(3)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Penyebab Pengembalian belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        pass
    
    def test_TC_PNBK_002(self):
        driver = self.driver
        print("test_TC_PNBR_002")
        driver.find_element(By.CSS_SELECTOR,"#fmpenyebab_pengembalian > option:nth-child(6)").click()
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Penyebab Pengembalian Lainnya belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        pass
    
    def test_TC_PNBK_003(self):
        driver = self.driver
        print("test_TC_PNBR_003")
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"#fmpenyebab_pengembalian > option:nth-child(2)").click()
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Nomor BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        
    def test_TC_PNBK_004(self):
        driver = self.driver
        print("test_TC_PNBR_004")

        driver.find_element(By.ID,"fmno_bast").send_keys("08/bast/2025")
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Tanggal BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(2)
        
    def test_TC_PNBK_005(self):
        driver = self.driver
        print("test_TC_PNBR_005")
        
        driver.find_element(By.ID,"fmtgl_bast").send_keys("testing non tgl")
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Tanggal BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        driver.find_element(By.ID,"fmtgl_bast").clear()
        time.sleep(2)
        
    def test_TC_PNBK_006(self):
        driver = self.driver
        print("test_TC_PNBR_006")
        
        next_day = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys(next_day)
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Penerima belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_007(self):
        driver = self.driver
        print("test_TC_PNBR_007")
        
        next_day = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

        driver.find_element(By.ID,"fmtgl_bast").clear()
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        driver.find_element(By.ID,"fmtgl_bast").send_keys(next_day)
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Penerima belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_008(self):
        driver = self.driver
        print("test_TC_PNBR_008")
        
        button(driver, By.ID, "fmpenerima_nama_button")
        
        time.sleep(2)
        checkbox(self.driver, identifier=1, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Pangkat Penerima belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_009(self):
        driver = self.driver
        print("test_TC_PNBR_009")
        
        self.driver.find_element(By.ID,"fmpenerima_pangkat").send_keys("4B")
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Kondisi Barang belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_010(self):
        driver = self.driver
        print("test_TC_PNBR_010")
        
        driver.find_element(By.CSS_SELECTOR,"#fmkondisi > option:nth-child(2)").click()
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Diinput Oleh belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_011(self):
        driver = self.driver
        print("test_TC_PNBR_011")
        
        driver.find_element(By.CSS_SELECTOR,"#fmdiinput_oleh > option:nth-child(2)").click()
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Diinput Nama belum dipilih!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
    def test_TC_PNBK_012(self):
        driver = self.driver
        print("test_TC_PNBR_012")
        
        button(driver, By.ID, "fmdiinput_nama_button")
        time.sleep(2)
        checkbox(self.driver, identifier=2, by="index", table_selector="#PegawaiPilih_cont_daftar > table")
        time.sleep(2)
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)

        button(driver, By.ID, "btSimpan")
        
        #se harus nya   
        # next_day = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        
        # time.sleep(2)
        # alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        # alert_text = alert.text.strip()
        # print(f"ℹ️ Alert text: {alert_text}")
        # expected_text = f"Tanggal Transaksi Pengembalian tidak lebih kecil dari Tanggal BAST! ({next_day})"
        # self.assertIn(expected_text, alert_text, f"Alert text mismatch, got: {alert_text}")
        # alert.accept()
        
    
    def test_ZZZ_998(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengembalianPeralatan")
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(3)
        checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(3)
        self.driver.find_element(By.PARTIAL_LINK_TEXT,"Batal").click()
        time.sleep(3)
        
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
            
    def test_ZZZ_999(self):
        logout(self.driver)
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
