from typing import Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)


def checkbox(
    driver: WebDriver,
    identifier,
    by: str = "id",
    timeout: int = 10,
    table_selector: Optional[str] = None,
) -> None:
    wait = WebDriverWait(driver, timeout)

    locator: Optional[Tuple[str, str]] = None
    el: WebElement

    if by == "id":
        locator = (By.ID, str(identifier))
        el = wait.until(EC.presence_of_element_located(locator))
    elif by == "index":
        selector = "input[type='checkbox']"
        if table_selector:
            selector = f"{table_selector} {selector}"
        boxes = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        if identifier >= len(boxes):
            raise IndexError(
                f"Hanya ada {len(boxes)} checkbox, index {identifier} tidak tersedia."
            )
        el = boxes[identifier]
    else:
        raise ValueError("Parameter 'by' harus 'id' atau 'index'.")

    if (
        el.tag_name.lower() == "input"
        and el.get_attribute("type") == "checkbox"
        and not el.is_displayed()
    ):
        el_id = el.get_attribute("id")
        if el_id:
            label = driver.find_element(By.CSS_SELECTOR, f'label[for="{el_id}"]')
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center', inline:'center'});", label
            )
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'label[for="{el_id}"]'))
            )
            label.click()
            return

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center', inline:'center'});", el
    )

    def not_covered(drv: WebDriver) -> bool:
        return drv.execute_script(
            """
            const el = arguments[0];
            const r = el.getBoundingClientRect();
            const x = Math.floor(r.left + r.width/2);
            const y = Math.floor(r.top + r.height/2);
            const e = document.elementFromPoint(x, y);
            return e === el || el.contains(e);
        """,
            el,
        )

    wait.until(lambda d: not_covered(d))

    if locator is not None:
        wait.until(EC.element_to_be_clickable(locator))
    else:
        wait.until(EC.element_to_be_clickable(el))

    try:
        el.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", el)
    except TimeoutException:
        driver.execute_script("arguments[0].click();", el)
