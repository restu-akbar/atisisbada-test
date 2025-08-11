import unittest
import os
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar
from helpers.logout_helper import logout
from helpers.nama_pemakai_check import nama_pemakai_check
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TC_PNBT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()

    #         cls.driver.quit()

    def setUp(self):
        load_dotenv()
        self.nibar = os.getenv("nibar")
        self.nama_pemakai = None

    def batal_helper(self):
        driver = self.driver
        driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        page = ModulPengamananPage(driver)
        self.assertTrue(
            page.is_loaded(page_name="Pengamanan"), "❌ Modul Pengamanan gagal dimuat"
        )
        time.sleep(1)
        filter_nibar(driver, self.nibar)
        time.sleep(1)
        checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:pengamananPeralatanTrans.Hapus()")

    def test_TC_PNBT_001(self):
        print("TC_PNBT_001")
        self.batal_helper()
        driver = self.driver
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        except TimeoutException:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()

        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        except TimeoutException:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        assert "Sukses Hapus Data" in alert_text, f"❌ Alert tidak sesuai: {alert_text}"
        alert.accept()
        print(
            f"[✅] TC_PNBT_001 berhasil — Pemakaian dengan nibar {self.nibar} terhapus"
        )
        print(
            "========================================================================"
        )

    def test_TC_PNBT_002(self):
        print("TC_PNBT_002")
        self.assertFalse(
            nama_pemakai_check(self).strip(),
            "[❌] Gagal: nama pemakai masih ada",
        )
        print("[✅] TC_PNBT_002 berhasil — Nama Identitas Pemakai sudah tidak ada")
        print(
            "========================================================================"
        )

    def test_TC_PNBT_003(self):
        print("TC_PNBT_003")
        self.batal_helper()
        driver = self.driver
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        except TimeoutException:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        except TimeoutException:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        assert "Tidak bisa dibatalkan, sudah Pengembalian!" in alert_text, (
            f"❌ Alert tidak sesuai: {alert_text}"
        )
        alert.accept()
        print(
            f"[✅] TC_PNBT_003 berhasil — Pemakaian dengan nibar {self.nibar} terhapus"
        )
        print(
            "========================================================================"
        )


if __name__ == "__main__":
    unittest.main()
