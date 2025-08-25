from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from components.button import button
from helpers.print_result import print_result


def save_get_alert(
    driver,
    expected=None,
    test_name="TEST_CASE",
    save_button="btSimpan",
    accept=True,
    timeout=5,
):
    button(driver, By.ID, save_button)
    actual = ""
    alert = None

    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        actual = alert.text or ""
    except TimeoutException:
        actual = ""

    if expected is not None:
        print_result(actual, expected, test_name)

    if alert:
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True
    else:
        return False

