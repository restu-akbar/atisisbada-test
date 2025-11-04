import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from components.dropdown import Dropdown
from components.form_input import form_input, get_value_form
from components.button import button
from components.checkbox import checkbox
from helpers.filter_nibar import filter_nibar_pembukuan
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from helpers.Pengamanan import PengamananPM, BatalPengamananPM

from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC


# python -m unittest tests.TC_MUTASI.TC_PEMINDAH_TANGANAN
class TC_PEMINDAH_TANGANAN(unittest.TestCase):
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
        TC_PEMINDAH_TANGANAN.nibar = os.getenv("nibar")
        time.sleep(2)
        driver.get(f"{cls.url}index.php?Pg=05&SPg=03&jns=tetap")
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()

    #         cls.driver.quit()

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

    def test_TC_PEMINDAH_TANGANAN_001(self):
        print("test_TC_PEMINDAH_TANGANAN_001")
        PengamananPM(self.driver, self.nibar)
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar, pengamanan=True)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        BatalPengamananPM(self.driver, self.nibar)

    def test_TC_PEMINDAH_TANGANAN_002(self):
        print("test_TC_PEMINDAH_TANGANAN_002")
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        self.flow_ubah()
        flow_batal(self.driver, self.url, self.nibar)

    def test_TC_PEMINDAH_TANGANAN_003(self):
        print("test_TC_PEMINDAH_TANGANAN_003")
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar, jenis=1)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        self.flow_ubah("index.php?Pg=10&bentuk=1")
        flow_batal(self.driver, self.url, self.nibar, "index.php?Pg=10&bentuk=1")

    def test_TC_PEMINDAH_TANGANAN_004(self):
        print("test_TC_PEMINDAH_TANGANAN_004")
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar, jenis=2)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        self.flow_ubah("index.php?Pg=10&bentuk=2")
        flow_batal(self.driver, self.url, self.nibar, "index.php?Pg=10&bentuk=2")

    def test_TC_PEMINDAH_TANGANAN_005(self):
        print("test_TC_PEMINDAH_TANGANAN_005")
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar, jenis=3)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        self.flow_ubah("index.php?Pg=10&bentuk=3")
        flow_batal(self.driver, self.url, self.nibar, "index.php?Pg=10&bentuk=3")

    def test_TC_PEMINDAH_TANGANAN_006(self):
        print("test_TC_PEMINDAH_TANGANAN_006")
        flow_pemindahtanganan_001(self.driver, self.url, self.nibar, jenis=4)
        TC_PEMINDAH_TANGANAN.switch_to_main_window(self.driver)
        time.sleep(2)
        self.flow_ubah("index.php?Pg=10&bentuk=4")
        flow_batal(self.driver, self.url, self.nibar, "index.php?Pg=10&bentuk=4")

    def flow_ubah(self, endpoint="index.php?Pg=10"):
        driver = self.driver
        driver.get(f"{self.url}{endpoint}")
        time.sleep(2)
        form_input(driver, By.ID, "fmIDBARANGCARI", self.__class__.nibar)
        button(driver, By.ID, "btTampil")
        time.sleep(2)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(2)
        href_button(driver, "javascript:Pindahtangan.Edit()")
        time.sleep(2)

        form_input(driver, By.ID, "nosk", "988")
        form_input(driver, By.ID, "kepada_nama", "Sulthan Aulia Rahman")
        form_input(driver, By.ID, "kepada_alamat", "Alamat Penerima")
        form_input(driver, By.ID, "uraian", "Testing Edited")
        form_input(driver, By.ID, "ket", "Keterangan Edited")
        time.sleep(4)

        button(
            driver,
            By.CSS_SELECTOR,
            "#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)",
        )
        save_get_alert(
            driver,
            expected="Sukses Simpan Data",
            with_button=False,
            test_name="TC_PEMINDAH_TANGANAN_002",
        )
        time.sleep(3)


def flow_batal(driver, url, nibar, endpoint="index.php?Pg=10"):
    driver.get(f"{url}{endpoint}")
    time.sleep(2)
    form_input(driver, By.ID, "fmIDBARANGCARI", nibar)
    button(driver, By.ID, "btTampil")
    time.sleep(2)
    checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
    time.sleep(2)
    href_button(driver, "javascript:Pindahtangan.Hapus()")
    time.sleep(2)

    alert = Alert(driver)
    alert_text = alert.text
    print(f"ℹ️ Alert muncul: {alert_text}")
    alert.accept()
    time.sleep(3)

    save_get_alert(
        driver,
        expected="Sukses Hapus Data",
        with_button=False,
        test_name="TC_PEMINDAH_TANGANAN_003",
    )

    time.sleep(3)


def flow_pemindahtanganan_001(driver, url, nibar, jenis=1, pengamanan=False):
    driver.get(f"{url}index.php?Pg=05&SPg=03&jns=tetap")
    filter_nibar_pembukuan(driver, nibar)
    time.sleep(1)
    checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
    time.sleep(1)
    href_button(driver, "javascript:pemindahtanganan_ins.pemindahtangananbaru()()")
    time.sleep(2)
    alert = Alert(driver)
    alert_text = alert.text
    print(f"ℹ️ Alert muncul: {alert_text}")
    alert.accept()
    time.sleep(1)

    handles = driver.window_handles
    if len(handles) > 1:
        driver.switch_to.window(handles[-1])
        time.sleep(2)
        form_input(driver, By.ID, "no_sk", "999123")

        Dropdown(driver, identifier="fmBENTUKPEMINDAHTANGANAN", value=jenis)
        time.sleep(3)
        form_input(driver, By.ID, "ket", "Auto testing Keterangan")
        time.sleep(3)
        button(driver, By.ID, "btsave")

    if not pengamanan:
        save_get_alert(
            driver,
            expected="Pemindahtanganan Selesai !",
            with_button=False,
            test_name="TC_PEMINDAH_TANGANAN_001",
        )
    else:
        save_get_alert(
            driver,
            expected="Ada 1 Kesalahan !",
            with_button=False,
            test_name="TC_PEMINDAH_TANGANAN_004",
        )
        errmsg = get_value_form(driver, By.ID, "errmsg")
        print(f"ℹ️ Error Message: {errmsg}")
        time.sleep(4)

    time.sleep(3)


if __name__ == "__main__":
    unittest.main()
