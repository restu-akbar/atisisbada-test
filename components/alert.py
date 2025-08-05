from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AlertHandler:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def accept_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

    def dismiss_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()

    def get_alert_text(self):
        alert = self.wait.until(EC.alert_is_present())
        return alert.text
