from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def form_input(driver, by, locator, text, timeout=10):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.presence_of_element_located((by, locator)))
    element.clear()
    element.send_keys(text)
    
def get_value_form(driver, by, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.presence_of_element_located((by, locator)))
    value = element.get_attribute("value")
    return value

def parse_currency(value: str) -> float:
    cleaned = value.replace('.', '').replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0
