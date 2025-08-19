from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def set_tgl_buku(driver, tanggal_lengkap: str):
    dd, mm, yyyy = tanggal_lengkap.split("-")
    ddmm = f"{dd}-{mm}"

    tgl_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fmtgl_buku_tgl"))
    )
    thn_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fmtgl_buku_thn"))
    )

    try:
        driver.find_element(
            By.XPATH,
            "//input[@id='fmtgl_buku_tgl']/following-sibling::img[contains(@class,'ui-datepicker-trigger')]",
        ).click()
    except Exception:
        pass

    driver.execute_script(
        """
        const tgl = arguments[0], thn = arguments[1], ddmm = arguments[2], yyyy = arguments[3];
        try { tgl.removeAttribute('readonly'); } catch(e) {}
        try { thn.removeAttribute('readonly'); } catch(e) {}
        tgl.value = ddmm;
        thn.value = yyyy;
    
        ['input','change','blur'].forEach(evt => {
            tgl.dispatchEvent(new Event(evt, { bubbles: true }));
            thn.dispatchEvent(new Event(evt, { bubbles: true }));
        });
    """,
        tgl_el,
        thn_el,
        ddmm,
        yyyy,
    )