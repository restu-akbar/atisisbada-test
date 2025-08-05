from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Dropdown:
    def __init__(self, driver, by, locator, timeout=10):
        self.driver = driver
        self.locator = (by, locator)
        self.wait = WebDriverWait(driver, timeout)

    def select_by_value(self, value):
        element = self.wait.until(EC.presence_of_element_located(self.locator))
        Select(element).select_by_value(value)

    def select_by_visible_text(self, text):
        element = self.wait.until(EC.presence_of_element_located(self.locator))
        Select(element).select_by_visible_text(text)
