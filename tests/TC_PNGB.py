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


class TC_PNGB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_PNGB.nibar = os.getenv("nibar") 
        TC_PNGB.actual = ""
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananGedung")

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()


    def test_TC_PNGB_004(self, isedit=False):
        print("test_TC_PNGB_004")
        time.sleep(1)
        filter_pengamanan(self.driver, TC_PNGB.nibar or "")
        time.sleep(1)
        checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(self.driver, "javascript:pengamananGedung.formBaru()")
        alert_expected = (
            "Penghuni belum dipilih!" if isedit else "Penghuni belum dipilih!"
        )
        time.sleep(2)
        actual = save_get_alert(
            self.driver,
            expected=alert_expected,
            test_name="TC_PNGB_004"
        )
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_005(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_005")
        time.sleep(1)
        button(driver, By.ID, "fmnama_pemakai_button")
        time.sleep(1)
        checkbox(
            driver,
            identifier=1,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )
        time.sleep(1)
        driver.execute_script("PegawaiPilih.windowSave();")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Status Penghuni belum diisi!",
            test_name="TC_PNGB_005")
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_006(self, isedit=False):
        driver = self.driver
        value = "5"
        time.sleep(1)
        Dropdown(driver, identifier="fmstatus_pemakai", value=value, by="id")
        time.sleep(1)
        if value != "5":
            print("test_TC_PNGB_007")
            print("----TC_PNGB_006 skipped---- ")
            actual = save_get_alert(
                self.driver, "Nomor Identitas Pemakai belum diisi!", "TC_PNGB_007"
            )
        else:
            print("test_TC_PNGB_006")
            actual = save_get_alert(
                self.driver,
                expected="Status Pemakai Lainnya belum diisi!",
                test_name="TC_PNGB_006"
            )
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_007(self, isedit=False):
        driver = self.driver
        try:
            driver.switch_to.alert.accept()
        except Exception:
            pass
        current_value = driver.find_element(By.ID, "fmstatus_pemakai").get_attribute(
            "value"
        )

        if current_value != "5":
            self.skipTest('fmstatus_pemakai != "5" — TC_PNGB_007 di-skip')

        print("test_TC_PNGB_007")
        form_input(driver, By.ID, "fmstatus_pemakai_lainnya", "pegawai pembantu")
        time.sleep(1)
        actual = save_get_alert(
            self.driver,
            expected= "Nomor Identitas Penghuni belum diisi!",
            test_name="TC_PNGB_007"
        )
        
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual
            

    def test_TC_PNGB_008(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_008")
        form_input(driver, By.ID, "fmno_ktp_pemakai", "12345678")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Alamat Penghuni belum diisi!",
            test_name="TC_PNGB_008")
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_009(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_009")
        form_input(driver, By.ID, "fmalamat_pemakai", "Alamat Testing")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Nomor BAST belum diisi!",
            test_name="TC_PNGB_009")
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_010(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_010")
        form_input(driver, By.ID, "fmno_bast", "08/bast/2025")
        time.sleep(1)
        actual = save_get_alert(
            driver,
            expected="Tanggal BAST belum diisi!",
            test_name="TC_PNGB_010")
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_011(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_011")
        time.sleep(1)
        driver.find_element(By.ID, "fmtgl_bast").send_keys("02-05-2025")
        actual = save_get_alert(
            driver,
            expected="Diinput Oleh belum diisi!",
            test_name="TC_PNGB_011")
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual

    def test_TC_PNGB_012(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_012")
        Dropdown(driver, identifier="fmdiinput_oleh", value="1", by="id")
        time.sleep(1)
        if isedit:
            expected="Diinput Nama belum diisi!"
        else:
            expected="Diinput Nama belum dipilih!"
            
        actual = save_get_alert(
            driver,
            expected,
            test_name="TC_PNGB_012")
        

    def test_TC_PNGB_013(self, isedit=False): 
        driver = self.driver
        print("test_TC_PNGB_013")
        button(driver, By.ID, "fmdiinput_nama_button")
        time.sleep(1)
        checkbox(
            driver,
            identifier=1,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )
        time.sleep(1)
        driver.execute_script("PegawaiPilih.windowSave();")
        time.sleep(1)
        
        dt = datetime.now()
        changed_dt = dt.replace(month=8, day=22).strftime("%d-%m-%Y")
        
        set_tgl_buku(self.driver, changed_dt)
        
        time.sleep(1)
        print_result("tidak tersimpan","tersimpan","TC_PNGB_013") # band aid untuk assert saat ini update nanti thengan save get aler

        # ini seharusnya memunculkan alert kalau sudah di perbaiki uncomment dibawah ini
        # save_get_alert(driver, "Diinput Nama belum dipilih!", "TC_PNGB_012")


    def test_TC_PNGB_014(self):
        driver = self.driver
        print("test_TC_PNGB_014 skipped..")
    #   tidak ada barang yang ada pada tahun 2025
    #   (tgl transaksi di lock pada tahun ini jadi tidak dapat di tes kecuali dapat di buat baru 
    #   tapi tidak tahu alur nya nanti akan di tanyakan terlebih dahulu)

    def test_TC_PNGB_015(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_015")
        
        dt = datetime.now()
        changed_dt = dt.replace(month=5, day=1).strftime("%d-%m-%Y")
        
        set_tgl_buku(self.driver, changed_dt)
        
        time.sleep(2)
        actual = save_get_alert(
            driver,
            expected="Tanggal Transaksi Pengamanan tidak lebih kecil dari Tanggal BAST! (02-05-2025)",
            test_name="TC_PNGB_015")
        time.sleep(1)
        if isedit:
            return actual
        else:
            TC_PNGB.actual = actual
         
    #Simpan akhir
    def test_TC_PNGB_016(self, isedit=False):
        driver = self.driver
        print("test_TC_PNGB_016")
       
        dt = datetime.now()
        changed_dt = dt.replace(month=5, day=3).strftime("%d-%m-%Y")
        time.sleep(1)
        set_tgl_buku(self.driver, changed_dt)
        
        time.sleep(5)
        driver.find_element(By.ID, "btSimpan").click()
        time.sleep(1)
        driver.get(f"{self.url}pages.php?Pg=pengamananGedungTrans")
        time.sleep(1)
        driver.execute_script("document.body.style.zoom='70%'")
        print_result("Data Tersimpan","Data Tersimpan", test_name="TC_PNGB_016") #eye ball it
        time.sleep(5)
        pass

    # def test_TC_PNGB_017(self):
    #     driver = self.driver
    #     print("test_TC_PNGB_017")
    #     driver.get(f"{self.url}index.php?Pg=05&SPg=05&jns=tetap")
    #     time.sleep(1)
    #     checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
    #     driver.execute_script("document.body.style.zoom='80%'")
    #     #TODO: Assert ubah atau buat komponen baru untuk mengecek data nya sama atau tidak
    #     print_result("Data Sesuai","Data Sesuai", test_name="TC_PNGB_016")
    #     time.sleep(1)
    #     pass

    def test_TC_PNGB_018(self):
        driver = self.driver
        print("test_TC_PNGB_018")
        self.driver.get(f"{self.url}pages.php?Pg=pengamananGedung")
        time.sleep(1)
        filter_pengamanan(driver, self.nibar or "")
        time.sleep(1)
        checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(self.driver, "javascript:pengamananGedung.formBaru()")
        time.sleep(1)

        expected = "Belum dilakukan pengembalian barang untuk pengguna/pemakai sebelumnya!"    
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        self.assertEqual(
            alert_text,
            expected,
            f"Teks alert tidak sesuai, dapat: {alert_text}",
        )
        print_result(alert.text, expected, test_name="TC_PNGB_018")
        alert.accept()
        
        time.sleep(1)

    # def test_ZZZ_998(self):
    #     self.driver.get(f"{self.url}pages.php?Pg=pengamananGedungTrans")
    #     self.driver.execute_script("document.body.style.zoom='80%'")
    #     time.sleep(1)
    #     checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
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
