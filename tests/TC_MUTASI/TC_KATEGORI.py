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
from helpers.print_result import print_result

from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC

#python -m unittest tests.TC_MUTASI.TC_KATEGORI
class TC_KATEGORI(unittest.TestCase):
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
        TC_KATEGORI.nibar = os.getenv("nibar")
        time.sleep(2)
        driver.get(f"{cls.url}index.php?Pg=05&SPg=03&jns=lain")
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

    # @unittest.skip("test")
    def test_TC_KATEGORI_001(self):
        print("test_TC_KATEGORI_001")
        driver = self.driver
        
        filter_nibar_pembukuan(driver, self.__class__.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:AsetLainLain.fmKategori('cidBI[]',1)")
        time.sleep(1)
        Dropdown(driver, "fkategori", 3)
        form_input(driver,By.ID,"fmKet","auto testing")
        time.sleep(3)
        button(driver,By.ID,"btProses")
        time.sleep(3)

        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Selesai",
            with_button=False,
            test_name="TC_KATEGORI_001",
        )
        time.sleep(2)
    
    # @unittest.skip("Bug")    
    def test_TC_KATEGORI_002(self):
        print("test_TC_KATEGORI_002")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=updKatAsetLainLain")
        time.sleep(3)
        form_input(driver, By.ID, "fmFiltNibar", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:updkatasetlainlain.formEdit()")
        time.sleep(3)
        button(driver,By.CSS_SELECTOR,"#fkategori > option:nth-child(1)")
        form_input(driver,By.ID,"fmket","test edited")
        time.sleep(5)
        button(driver,By.ID,"btSimpan")
        time.sleep(5)
        
        save_get_alert(
            driver,
            expected="Kategori Baru belum dipilih!",
            with_button=False,
            test_name="TC_KATEGORI_002",
        )
        
    # @unittest.skip("Bug")
    def test_TC_KATEGORI_003(self):
        print("test_TC_KATEGORI_003")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=updKatAsetLainLain")
        time.sleep(3)
        form_input(driver, By.ID, "fmFiltNibar", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:updkatasetlainlain.formEdit()")
        time.sleep(3)
        button(driver,By.CSS_SELECTOR,"#fkategori > option:nth-child(6)")
        form_input(driver,By.ID,"fmket","test edited")
        time.sleep(5)
        button(driver,By.ID,"btSimpan")
        time.sleep(2)
        print_result("ter edit","ter edit", "TC_KATEGORI_003")
        
    
            
    # @unittest.skip("Bug")
    def test_TC_KATEGORI_004(self):
        print("test_TC_KATEGORI_004")
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=updKatAsetLainLain")
        time.sleep(3)
        form_input(driver, By.ID, "fmFiltNibar", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:updkatasetlainlain.Hapus()")
        
        
        save_get_alert(
            driver,
            expected="Hapus 1 Data ?",
            with_button=False,
            test_name="TC_KATEGORI_004",
        )
        
        save_get_alert(
            driver,
            expected="Sukses Hapus Data",
            with_button=False,
            test_name="TC_KATEGORI_004",
        )
        
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()