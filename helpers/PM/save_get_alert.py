from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from components.button import button
from helpers.print_result import print_result



import unicodedata
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def normalize_text(text: str) -> str:
    # Normalize Unicode (remove weird hidden chars)
    return unicodedata.normalize("NFKC", text).strip()

def save_get_alert(
    driver,
    expected=None,
    test_name="TEST_CASE",
    save_button="btSimpan",
    accept=True,
    timeout=5,
    with_button=True
):
    if with_button:
        button(driver, By.ID, save_button)
        actual = ""
        alert = None

    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        actual = alert.text or ""
    except TimeoutException:
        actual = ""

    if expected is not None:
        # Normalize before comparison
        actual_norm = normalize_text(actual)
        expected_norm = normalize_text(expected)

        if expected is not None:
            print_result(actual_norm, expected_norm, test_name)

    if alert:
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True
    else:
        return False

