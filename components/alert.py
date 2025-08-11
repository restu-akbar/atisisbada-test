from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.print_result import print_result
from selenium.webdriver.common.alert import Alert
import unittest

        
def alert_handle(self, alert, expected_msg, test_name="TEST_CASE"):
    alert_text = alert.text
    print(f"ℹ️ Alert muncul: {alert_text}")
    self.assertEqual(alert_text, expected_msg, f"Teks alert tidak sesuai, dapat: {alert_text}")
    print_result(alert_text, expected_msg, test_name)
    alert.accept()