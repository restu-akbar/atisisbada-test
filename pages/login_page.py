from selenium.webdriver.common.by import By
from components.button import button
from components.form_input import FormInput


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        user_input = FormInput(self.driver, By.ID, "user")
        user_input.enter_text(username)

        password_input = FormInput(self.driver, By.ID, "password")
        password_input.enter_text(password)

        button(self.driver, By.ID, "bt_ok")
