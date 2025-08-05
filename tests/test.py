import unittest
import os
from dotenv import load_dotenv

from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.login_helper import login


class TestPengamanan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_buka_modul_pengamanan(self):
        self.driver.get(self.url)

        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")

        if not user or not password:
            raise ValueError("email atau password tidak ada di file .env")

        login(self.driver, user, password)
        href_button(self.driver, "pages.php?Pg=pemeliharaan_daftar")


if __name__ == "__main__":
    unittest.main()
