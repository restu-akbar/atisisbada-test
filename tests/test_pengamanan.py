import unittest
import os
from dotenv import load_dotenv
from helpers.driver_setup import create_driver
from pages.login_page import LoginPage
from pages.modul_pengamanan_page import ModulPengamananPage


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

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_buka_modul_pengamanan(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatan")
        page = ModulPengamananPage(self.driver)
        self.assertTrue(page.is_loaded(), "❌ Modul Pengamanan gagal dimuat")


if __name__ == "__main__":
    unittest.main()
