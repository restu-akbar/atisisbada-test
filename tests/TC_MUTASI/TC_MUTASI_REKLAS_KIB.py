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

#python -m unittest tests.TC_MUTASI.TC_MUTASI_REKLAS_KIB
class TC_MUTASI_REKLAS_KIB(unittest.TestCase):
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
        TC_MUTASI_REKLAS_KIB.nibar = os.getenv("nibar")
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

    # @unittest.skip("test")
    def test_TC_MUTASI_REKLAS_KIB_001(self):
        print("test_TC_MUTASI_REKLAS_KIB_001")
        driver = self.driver
        
        filter_nibar_pembukuan(driver, self.__class__.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:Reclass.reClass()")
        time.sleep(2)
        
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[-1])
            time.sleep(2)
            button(driver, By.ID, "caribarang")
            time.sleep(2)
            form_input(driver, By.ID, "fmKODE", "1.3.2.01.03.05.010")
            time.sleep(2)
            button(driver, By.ID, "btTampil")
            time.sleep(2)
            el = driver.find_element(By.PARTIAL_LINK_TEXT, "1.3.2.01.03.05.010")
            el.click()
            time.sleep(2)


        form_input(driver, By.ID, "ket", "Reklas KIB KIB Sama")
        
        time.sleep(2)
        href_button(driver, "javascript:Reclass.Simpan2()")
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Tidak boleh reklas ke KIB yang sama",
            with_button=False,
            test_name="TC_MUTASI_REKLAS_KIB_001",
        )
        time.sleep(1)
        
        TC_MUTASI_REKLAS_KIB.switch_to_main_window(driver) 
            
    # @unittest.skip("test 2")
    def test_TC_MUTASI_REKLAS_KIB_002(self):
        print("test_TC_MUTASI_REKLAS_KIB_002")
        driver = self.driver
        driver.get(f"{self.url}index.php?Pg=05")
        time.sleep(1)
        filter_nibar_pembukuan(driver, self.__class__.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:Reclass.reClass()")
        time.sleep(2)
        
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[-1])
            time.sleep(2)
            button(driver, By.ID, "caribarang")
            time.sleep(2)
            form_input(driver, By.ID, "fmKODE", "1.3.5.02.01.01.001")
            time.sleep(2)
            button(driver, By.ID, "btTampil")
            time.sleep(2)
            el = driver.find_element(By.PARTIAL_LINK_TEXT, "1.3.5.02.01.01.001")
            el.click()
            time.sleep(2)

        form_input(driver, By.ID, "ket", "Reklas KIB KIB Berbeda")
        
        time.sleep(2)
        href_button(driver, "javascript:Reclass.Simpan2()")
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Sukses Reclass !",
            with_button=False,
            test_name="TC_MUTASI_REKLAS_KIB_002",
        )
        time.sleep(1)
        
        
        TC_MUTASI_REKLAS_KIB.switch_to_main_window(driver) 
        
    def test_TC_MUTASI_REKLAS_KIB_003(self):
        print("test_TC_MUTASI_REKLAS_KIB_003")
        driver = self.driver
        driver.get(f"{self.url}index.php?Pg=09&SPg=01&SSPg=03&mutasi=2&menu=pelaporan")
        time.sleep(2)
        form_input(driver, By.ID, "fmidawal", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:Batal_Reclass()")
        time.sleep(2)
        
        alert = Alert(driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        
        time.sleep(2)
        
        save_get_alert(
            driver,
            expected="Data sukses di batalkan",
            with_button=False,
            test_name="TC_MUTASI_REKLAS_KIB_003",
        )
        
        time.sleep(2)

if __name__ == "__main__":
    unittest.main()