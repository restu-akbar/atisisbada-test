from selenium.webdriver.common.by import By
from components.form_input import FormInput
from components.button import Button


def login(driver, username, password):
    user_input = FormInput(driver, By.ID, "user")
    user_input.enter_text(username)

    password_input = FormInput(driver, By.ID, "password")
    password_input.enter_text(password)

    login_button = Button(driver, By.ID, "bt_ok")
    login_button.click()
