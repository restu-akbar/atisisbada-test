import unittest
import os
from dotenv import load_dotenv
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
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
        
    def test_TC_PNBR_004(self):
        print("test_TC_PNBR_004")
        page = ModulPengamananPage(self.driver)
        logout(self.driver)
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
