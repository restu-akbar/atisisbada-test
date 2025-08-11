import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from components.button import button
from components.checkbox import checkbox
from components.form_input import form_input
from components.href_button import href_button


def nama_pemakai_check(self):
    driver = self.driver
    driver.get(f"{self.url}index.php?Pg=05")
    time.sleep(1)
    form_input(driver, By.ID, "nodata", self.nibar)
    time.sleep(1)
    button(driver, By.XPATH, "//input[@value='Tampilkan']")
    time.sleep(1)
    checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
    time.sleep(1)
    href_button(driver, "javascript:prosesEdit()")
    driver.switch_to.window(driver.window_handles[-1])

    try:
        nama_pemakai = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.ID, "nama2")))
            .get_attribute("value")
        )
        return nama_pemakai or ""
    except Exception as e:
        print(f"Gagal mengambil nama pemakai: {e}")
        return ""
