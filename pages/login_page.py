from selenium.webdriver.common.by import By
from components.button import button
from components.form_input import form_input


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        form_input(self.driver, By.ID, "user", username)

        form_input(self.driver, By.ID, "password", password)

        button(self.driver, By.ID, "bt_ok")
