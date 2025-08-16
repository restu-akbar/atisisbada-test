from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from helpers.print_result import print_result


def save_get_alert(
    driver, expected=None, test_name="TEST_CASE", accept=True, timeout=5
):
    driver.find_element(By.ID, "btSimpan").click()

    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
    except TimeoutException:
        raise AssertionError(
            f"[❌] {test_name} gagal: Alert tidak muncul dalam {timeout} detik."
        )

    actual = alert.text

    if expected is not None:
        print_result(actual, expected, test_name)

    if accept:
        alert.accept()
    else:
        alert.dismiss()
