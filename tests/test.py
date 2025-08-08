import unittest
import os
from dotenv import load_dotenv

from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.login_helper import login
from helpers.logout_helper import logout

from navigation.navigate import to_peralatan_dan_mesin 
import time


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
        to_peralatan_dan_mesin(self.driver)  # Pass driver instead of self
        logout(self.driver)
        time.sleep(3) # agar keliahatan apakah sudah logout atau belum



if __name__ == "__main__":
    unittest.main()
