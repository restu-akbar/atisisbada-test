import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from components.dropdown import Dropdown
from components.form_input import form_input
from components.button import button
from components.checkbox import checkbox
from helpers.filter_nibar import filter_nibar_pembukuan
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert

from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC

#python -m unittest tests.TC_MUTASI.TC_MUTASI_KOREKSI_HARGA
class TC_MUTASI_KOREKSI_HARGA(unittest.TestCase):
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
        TC_MUTASI_KOREKSI_HARGA.nibar = os.getenv("nibar")
        time.sleep(2)
        driver.get(f"{cls.url}index.php?Pg=05")
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

    #@unittest.skip("test")
    def test_TC_MUTASI_KOREKSI_HARGA_001(self):
        print("test_TC_MUTASI_KOREKSI_HARGA_001")
        driver = self.driver
        
        filter_nibar_pembukuan(driver, self.__class__.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:updatebarang.formUpdate()")
        time.sleep(2)
        
        
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[-1]) # ithink this is making the problem because after the alert the windows is deleted so i switch again
            time.sleep(2)
            form_input(driver, By.ID, "no_bast", "05/BAST/2025") #this actually printed

        
        Dropdown(driver, "trans", "1")
        time.sleep(1)
        form_input(driver, By.ID, "hrg_baru", "1000000000")
        time.sleep(1)
        form_input(driver, By.ID, "ket_koreksi", "testing")
        time.sleep(1)
        href_button(driver, "javascript:updatebarang.SimpanKoreksi()")
        time.sleep(1)
        
        save_get_alert(
            driver,
            expected="Data berhasil di simpan !",
            with_button=False,
            test_name="TC_MUTASI_KOREKSI_HARGA_001",
        )
        time.sleep(3)
        
        TC_MUTASI_KOREKSI_HARGA.switch_to_main_window(driver) 
            
    @unittest.skip("Bug")
    def test_TC_MUTASI_KOREKSI_HARGA_002(self):
        print("test_TC_MUTASI_KOREKSI_HARGA_002")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=Koreksi&menu=pelaporan")
        time.sleep(3)
        form_input(driver, By.ID, "idbi_awal", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:Koreksi.Edit()")
        form_input(driver, By.ID, "hrg_baru", "3000000000")
        button(driver,By.CSS_SELECTOR, "input[type='button'][value='Simpan']")
        
        save_get_alert(
            driver,
            expected="Data berhasil di simpan !",
            with_button=False,
            test_name="TC_MUTASI_KOREKSI_HARGA_002",
        )
        
        time.sleep(5)
        
        
    #@unittest.skip("test")
    def test_TC_MUTASI_KOREKSI_HARGA_003(self):
        print("test_TC_MUTASI_KOREKSI_HARGA_003")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=Koreksi&menu=pelaporan")
        time.sleep(3)
        form_input(driver, By.ID, "idbi_awal", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=-1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:Koreksi.Hapus()")
        time.sleep(2)
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        
        save_get_alert(
            driver,
            expected="Sukses Batalkan",
            with_button=False,
            test_name="TC_MUTASI_KOREKSI_HARGA_003",
        )

if __name__ == "__main__":
    unittest.main()