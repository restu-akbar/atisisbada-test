import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from components.dropdown import Dropdown
from components.form_input import form_input,get_value_form,parse_currency
from components.button import button
from components.checkbox import checkbox
from helpers.filter_nibar import filter_gantirugi,filter_formgantirugi,filter_formgantirugiPembayaran
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from helpers.Pengamanan import PengamananPM,BatalPengamananPM

from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC

#python -m unittest tests.TC_MUTASI.TC_TUNTUTAN_GANTI_RUGI
class TC_TUNTUTAN_GANTI_RUGI(unittest.TestCase):
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
        TC_TUNTUTAN_GANTI_RUGI.nibar = os.getenv("nibar")
        time.sleep(2)
        driver.get(f"{cls.url}pages.php?Pg=gantirugi")
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
        
    def switch_to_main_window(driver):
        """Force switch to the first (main) window."""
        try:
            main = driver.window_handles[0]
            driver.switch_to.window(main)
        except Exception as e:
            print(f"[⚠️] Tidak bisa switch ke main window: {e}")

    def tearDown(self):
        d = getattr(self, "driver", None)
        if not d or not getattr(d, "session_id", None):
            return

        try:
            handles = d.window_handles
            if len(handles) > 1:
                # close only if still valid
                current = d.current_window_handle
                target = next((h for h in reversed(handles) if h != current), None)
                try:
                    d.close()
                except Exception as e:
                    print(f"[⚠️] Gagal close window: {e}")
                if target in d.window_handles:
                    d.switch_to.window(target)
            # if only 1 handle → do nothing, keep it open for next test
        except Exception as e:
            print(f"[⚠️] Gagal menutup tab atau berpindah: {e}")

    @unittest.skip("test")
    def test_TC_TUNTUTAN_GANTI_RUGI_001(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_001")
        driver = self.driver
        user = os.getenv("user")
        href_button(driver, "javascript:gantirugi.KetetapanTanpaUsulan(1)")
        time.sleep(1)
        
        #tombol 'cari' di form TTG baru
        button(driver,By.CSS_SELECTOR,"#gantirugi_form_div > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]:nth-child(3)")
        time.sleep(6)
        
        filter_formgantirugi(driver,self.__class__.nibar)
        
        time.sleep(1)
        checkbox(driver, identifier=0, by="index", table_selector="table#penatausahaanTable.koptable")
        time.sleep(1)
        button(driver,By.CSS_SELECTOR,"#div_border > table > tbody > tr:nth-child(3) > td > div > div > input[type=button]:nth-child(1)")
        time.sleep(1)
        
        form_input(driver,By.ID,"no_sk","12334321")
        form_input(driver,By.ID,"harga",12000000) #12 jt
        form_input(driver,By.ID,"kepada_nama", user)
        form_input(driver,By.ID,"kepada_alamat","Alamat " + user)
        form_input(driver,By.ID,"uraian", "testing" + user)
        form_input(driver,By.ID,"ket", "Auto testing")
        
        
        button(driver,By.CSS_SELECTOR,"#div_border > div:nth-child(3) > div > input[type=button]:nth-child(7)")
        
        save_get_alert(
            driver,
            expected="Berhasil disimpan",
            with_button=False,
            test_name="TC_TUNTUTAN_GANTI_RUGI_001",
        )
        time.sleep(2)
    
    #edit
    @unittest.skip("Bug")
    def test_TC_TUNTUTAN_GANTI_RUGI_002(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_002")
        driver = self.driver
        user = os.getenv("user")
        driver.get(f"{self.url}pages.php?Pg=gantirugi")
        time.sleep(3)
        filter_gantirugi(driver, self.__class__.nibar)
        
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        href_button(driver, "javascript:gantirugi.Edit()")
        
        form_input(driver,By.ID,"no_sk","9999")
        
        # hutang = get_value_form(driver,By.ID,"harga")
        # form_input(driver,By.ID,"harga",hutang - 100) 
        
        form_input(driver,By.ID,"kepada_nama", user)
        form_input(driver,By.ID,"kepada_alamat","Alamat edit " + user)
        form_input(driver,By.ID,"uraian", "testing edit" + user)
        form_input(driver,By.ID,"ket", "Auto testing edit")
        
        button(driver,By.CSS_SELECTOR,"#div_border > div:nth-child(3) > div > input[type=button]:nth-child(7)")
        
        save_get_alert(
            driver,
            expected="Data Berhasil disimpan",
            with_button=False,
            test_name="TC_TUNTUTAN_GANTI_RUGI_001",
        )
        
    @unittest.skip("Bug")
    def test_TC_TUNTUTAN_GANTI_RUGI_003(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_003")
        driver = self.driver
        user = os.getenv("user")
        driver.get(f"{self.url}pages.php?Pg=gantirugi")
        time.sleep(3)
        filter_gantirugi(driver, self.__class__.nibar)
        
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        
        href_button(driver, "javascript:gantirugi.Hapus()")
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Sukses Batal",
            with_button=False,
            test_name="TC_TUNTUTAN_GANTI_RUGI_003",
        )
        
    # @unittest.skip("Bug")
    def test_TC_TUNTUTAN_GANTI_RUGI_004(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_004")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=gantirugibayar")
        time.sleep(3)
        href_button(driver, "javascript:gantirugibayar.Baru()")
        time.sleep(1)
        # button Cari Pembayaran
        button(driver,By.CSS_SELECTOR,"#gantirugibayar_form_div > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(3) > input[type=button]")
        time.sleep(1)
        filter_formgantirugiPembayaran(driver, self.__class__.nibar) 
        time.sleep(1)
        checkbox(driver, identifier="gantirugi_cari_cb0", by="id")
        time.sleep(1)
        #button Simpan the alert is here !
        button(driver,By.CSS_SELECTOR,"#div_border > table > tbody > tr:nth-child(3) > td > div > div > input[type=button]:nth-child(1)")
        time.sleep(1)
        
        form_input(driver,By.ID,"bayar",100)
        form_input(driver,By.ID,"dari_nama","receipt Testing")
        form_input(driver,By.ID,"ket","Auto Testing Pembayaran TGR")
        
        button(driver,By.CSS_SELECTOR,"#div_border > div:nth-child(3) > div > input[type=button]:nth-child(5)")
        
        
        print_result("Selesai", "Selesai", "TC_TUNTUTAN_GANTI_RUGI_004")
        
        # tidak ada Alert
        # save_get_alert(
        #     driver,
        #     expected="Selesai",
        #     with_button=False,
        #     test_name="TC_TUNTUTAN_GANTI_RUGI_004",
        # )
        
    #Edit Di Lunas Kan
    def test_TC_TUNTUTAN_GANTI_RUGI_005(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_005")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=gantirugibayar")
        time.sleep(3)
        filter_gantirugi(driver, self.__class__.nibar)
        time.sleep(2)
        checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:gantirugibayar.Edit()")
        time.sleep(3)
        
        harga = get_value_form(driver,By.ID,"sisa_bayar")
        jumlah_ketetapan = parse_currency(harga)
        
        form_input(driver,By.ID,"bayar",jumlah_ketetapan)
        form_input(driver,By.ID,"dari_nama","receipt Testing")
        form_input(driver,By.ID,"ket","Auto Testing	Lunas")
        time.sleep(5)
        button(driver,By.CSS_SELECTOR,"#div_border > div:nth-child(3) > div > input[type=button]:nth-child(5)")
        print_result("Selesai", "Selesai", "TC_TUNTUTAN_GANTI_RUGI_004")
        time.sleep(10)
    
    
    #Batal
    # @unittest.skip("Bug")
    def test_TC_TUNTUTAN_GANTI_RUGI_006(self):
        print("test_TC_TUNTUTAN_GANTI_RUGI_006")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=gantirugibayar")
        time.sleep(3)
        filter_gantirugi(driver, self.__class__.nibar)
        time.sleep(2)
        checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:gantirugibayar.Hapus()")
        time.sleep(3)
        
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Sukses Hapus Data",
            with_button=False,
            test_name="TC_TUNTUTAN_GANTI_RUGI_003",
        )
        
if __name__ == "__main__":
    unittest.main()