from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Button:
    def __init__(self, driver, by, locator, timeout=10):
        self.driver = driver
        self.locator = (by, locator)
        self.wait = WebDriverWait(driver, timeout)

    def click(self):
        element = self.wait.until(EC.element_to_be_clickable(self.locator))
        element.click()
