from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormInput:
    def __init__(self, driver, by, locator, timeout=10):
        self.driver = driver
        self.locator = (by, locator)
        self.wait = WebDriverWait(driver, timeout)

    def enter_text(self, text):
        element = self.wait.until(EC.presence_of_element_located(self.locator))
        element.clear()
        element.send_keys(text)
