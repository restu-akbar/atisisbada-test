from typing import Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    StaleElementReferenceException,
)


def checkbox(
    driver: WebDriver,
    identifier,
    by: str = "id",
    timeout: int = 10,
    table_selector: Optional[str] = None,
) -> None:
    wait = WebDriverWait(driver, timeout)

    # --- Build locator / selector ---
    locator: Optional[Tuple[str, str]] = None
    selector: Optional[str] = None

    if by == "id":
        locator = (By.ID, str(identifier))
    elif by == "index":
        selector = "input[type='checkbox']"
        if table_selector:
            selector = f"{table_selector} {selector}"
    else:
        raise ValueError("Parameter 'by' harus 'id' atau 'index'.")

    def fetch_el() -> WebElement:
        if locator:
            wait.until(EC.presence_of_element_located(locator))
            return driver.find_element(*locator)
        else:
            assert selector is not None

            def list_has_index(drv: WebDriver) -> bool:
                els = drv.find_elements(By.CSS_SELECTOR, selector)
                return len(els) > int(identifier)

            wait.until(list_has_index)
            return driver.find_elements(By.CSS_SELECTOR, selector)[int(identifier)]

    def try_click_via_label(el: WebElement) -> bool:
        try:
            if (
                el.tag_name.lower() == "input"
                and el.get_attribute("type") == "checkbox"
                and not el.is_displayed()
            ):
                el_id = el.get_attribute("id")
                if el_id:
                    label_loc = (By.CSS_SELECTOR, f'label[for="{el_id}"]')
                    lab = wait.until(EC.element_to_be_clickable(label_loc))
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center', inline:'center'});",
                        lab,
                    )
                    lab.click()
                    return True
        except StaleElementReferenceException:
            pass
        return False

    def wait_not_covered(el_supplier) -> None:
        def _ok(_):
            try:
                el = el_supplier()
                return driver.execute_script(
                    """
                    const el = arguments[0];
                    if (!el || !el.isConnected) return false;
                    const r = el.getBoundingClientRect();
                    const x = Math.floor(r.left + r.width/2);
                    const y = Math.floor(r.top + r.height/2);
                    const e = document.elementFromPoint(x, y);
                    return e === el || el.contains(e);
                    """,
                    el,
                )
            except StaleElementReferenceException:
                return False

        wait.until(_ok)

    last_err = None
    for _ in range(3):
        try:
            el = fetch_el()

            if try_click_via_label(el):
                return

            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center', inline:'center'});",
                    el,
                )
            except StaleElementReferenceException:
                continue

            wait_not_covered(fetch_el)

            if locator:
                wait.until(EC.element_to_be_clickable(locator))
                el = fetch_el()
            else:

                def is_clickable(_):
                    try:
                        e = fetch_el()
                        return e.is_displayed() and e.is_enabled()
                    except StaleElementReferenceException:
                        return False

                wait.until(is_clickable)
                el = fetch_el()

            try:
                el.click()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                try:
                    driver.execute_script("arguments[0].click();", fetch_el())
                except StaleElementReferenceException:
                    continue
            return

        except (StaleElementReferenceException, TimeoutException) as e:
            last_err = e
            continue

    if last_err:
        raise last_err
