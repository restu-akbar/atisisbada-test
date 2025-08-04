import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

from helpers.driver_setup import create_driver


class LahKerjaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_loginLahKerja(self):
        self.driver.get(self.url)

        load_dotenv()
        email = os.getenv("email")
        password = os.getenv("password")

        if not email or not password:
            raise ValueError("email atau password tidak ada di file .env")

        emailInput = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        emailInput.send_keys(email)

        passwordInput = self.wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        passwordInput.send_keys(password)

        login_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()

        self.wait.until(lambda driver: "dashboard" in driver.current_url)
        self.assertIn("dashboard", self.driver.current_url)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Pengaturan']]")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//a[@href='{self.url}/master/cuti-sakit']",
                )
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[@href='{self.url}/master/cuti-sakit/create']")
            )
        ).click()


if __name__ == "__main__":
    unittest.main()
