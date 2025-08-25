from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def clear_readonly_input(driver, by, locator: str, timeout: int = 10):
    wait = WebDriverWait(driver, timeout)
    elem = wait.until(EC.presence_of_element_located((by, locator)))

    driver.execute_script(
        """
        arguments[0].removeAttribute('readonly');
        arguments[0].removeAttribute('disabled');
    """,
        elem,
    )

    try:
        elem.clear()
    except Exception:
        elem.click()
        elem.send_keys(Keys.CONTROL, "a")
        elem.send_keys(Keys.DELETE)

    return elem
