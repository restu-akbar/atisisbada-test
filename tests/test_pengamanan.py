import unittest
import os
from dotenv import load_dotenv
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from components.dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
import time


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
        self.driver.execute_script("document.body.style.zoom='80%'")

        
    def test_TC_PNBR_004(self):
        driver = self.driver
        print("test_TC_PNBR_004")
        time.sleep(2)
        driver.find_element(By.ID,"pengamananPeralatan_cb0").click()
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
        driver.find_element(By.ID,"PegawaiPilih_cb0").click()
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
        driver.find_element(By.ID,"fmno_bast").send_keys("08/bast/2023")
        
        time.sleep(2)
        driver.find_element(By.ID,"btSimpan").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(alert_text, "Tanggal BAST belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        time.sleep(1)
        pass
        
    
    def test_TC_PNBR_011(self):
        driver = self.driver
        print("test_TC_PNBR_011")
        driver.find_element(By.CLASS_NAME,"ui-datepicker-trigger").click()
        time.sleep(1)
        
        date_element = driver.find_element(
            By.XPATH,
            "//td[contains(@class, 'ui-datepicker-week-end') and contains(@class, 'ui-datepicker-today')]"
        )

        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_element)
        time.sleep(0.5)  # Small delay to ensure scroll animation finishes
        date_element.click()
        
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
        print("test_TC_PNBR_005")
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
    
    def test_TC_PNBR_013(self):
        driver = self.driver
        print("test_TC_PNBR_013")
        time.sleep(2)
        driver.find_element(By.ID,"fmdiinput_nama_button").click()
        time.sleep(2)
        driver.find_element(By.ID,"PegawaiPilih_cb1").click()
        time.sleep(1)
        
        pilih_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)'))
        )
        driver.execute_script("PegawaiPilih.windowSave();", pilih_button)
        
        
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"#div_fmtgl_buku > div:nth-child(3) > div > img").click
        time.sleep(2)
        driver.find_element(By.CLASS_NAME,"#ui-datepicker-div > table > tbody > tr:nth-child(1) > td:nth-child(6) > a").click()
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        #hardcode dulu tgl nya
        self.assertEqual(alert_text, "Tanggal Transaksi Pengamanan tidak lebih kecil dari Tanggal BAST! (10-08-2025)", f"Teks alert tidak sesuai, dapat: {alert_text}")
        alert.accept()
        pass
    
    # def test_TC_PNBR_014(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_014")ui-state-default ui-state-highlight
    #     time.sleep(2)
        
    #     time.sleep(2)
    #     driver.find_element(By.CSS_SELECTOR,"#div_fmtgl_buku > div:nth-child(3) > div > img").click
    #     time.sleep(2)
    #     driver.find_element(By.CLASS_NAME,"#ui-datepicker-div > table > tbody > tr:nth-child(1) > td:nth-child(6) > a").click()
    #     time.sleep(2)
        
    #     time.sleep(2)
    #     driver.find_element(By.ID,"btSimpan").click()
    #     time.sleep(2)
        
    #     alert = Alert(driver)
    #     alert_text = alert.text
    #     print(f"ℹ️ Alert muncul: {alert_text}")
    #     self.assertEqual(alert_text, "Status Pemakai belum diisi!", f"Teks alert tidak sesuai, dapat: {alert_text}")
    #     alert.accept()
    #     pass
    
    # def test_TC_PNBR_015(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_005")
    #     pass
    # def test_TC_PNBR_016(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_005")
    #     pass
    # def test_TC_PNBR_017(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_005")
    #     pass
    
    # def test_TC_PNBR_018(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_005")
    #     pass
            
    def test_ZZZ_999(self):
        logout(self.driver)
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
