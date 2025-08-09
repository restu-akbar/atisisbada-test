from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def checkbox(driver, identifier, by="id", timeout=10, table_selector=None):
    wait = WebDriverWait(driver, timeout)

    try:
        if by == "id":
            checkbox_el = wait.until(
                EC.element_to_be_clickable((By.ID, str(identifier)))
            )

        elif by == "index":
            selector = "input[type='checkbox']"
            if table_selector:
                selector = f"{table_selector} {selector}"

            checkboxes = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )

            if identifier >= len(checkboxes):
                raise IndexError(
                    f"Hanya ada {len(checkboxes)} checkbox, index {identifier} tidak tersedia."
                )

            checkbox_el = wait.until(EC.element_to_be_clickable(checkboxes[identifier]))

        else:
            raise ValueError("Parameter 'by' harus 'id' atau 'index'.")

        checkbox_el.click()

    except Exception as e:
        raise Exception(
            f"Checkbox dengan {by}='{identifier}' tidak ditemukan atau tidak bisa diklik: {e}"
        )
