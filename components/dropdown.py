from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def Dropdown(driver, identifier, value, by="id", timeout=10, dropdown_selector=None):
    """Memilih opsi dari elemen dropdown (<select> atau kustom).

    Fungsi ini mendukung dropdown seperti `<select id="fmpenyebab_pengembalian">`
    dengan memilih opsi berdasarkan atribut `value`. Elemen dapat ditemukan
    menggunakan ID, indeks, atau XPath, dengan logika serupa dengan fungsi `checkbox`.

    Args:
        driver: Objek Selenium WebDriver (misalnya, `webdriver.Chrome()`).
        identifier: Pengenal elemen dropdown. Bergantung pada `by`:
            - `by="id"`: ID elemen (misalnya, `"fmpenyebab_pengembalian"`).
            - `by="index"`: Indeks elemen `<select>` (dimulai dari 0).
            - `by="xpath"`: Jalur XPath penuh (misalnya, `/html/body/div[1]/.../select`).
        value: Nilai atribut `value` dari opsi yang ingin dipilih
            (misalnya, `"1"`, `"2"` untuk `<option value="2">2. Purnatugas /Pensiun</option>`).
        by: Metode untuk menemukan elemen: `"id"` (default), `"index"`, atau `"xpath"`.
        timeout: Waktu tunggu (detik) hingga elemen dapat diklik.
        dropdown_selector: Pemilih CSS untuk membatasi pencarian elemen `<select>`
            saat `by="index"` (misalnya, `".form-container"`). Tidak digunakan untuk
            `by="id"` atau `by="xpath"`.

    Raises:
        ValueError: Jika `by` bukan `"id"`, `"index"`, atau `"xpath"`.
        IndexError: Jika `identifier` melebihi jumlah elemen `<select>` saat `by="index"`.
        Exception: Jika dropdown tidak ditemukan atau opsi tidak dapat dipilih.
    """
    wait = WebDriverWait(driver, timeout)

    try:
        if by == "id":
            dropdown_el = wait.until(
                EC.element_to_be_clickable((By.ID, str(identifier)))
            )
        elif by == "index":
            selector = "select"
            if dropdown_selector:
                selector = f"{dropdown_selector} {selector}"

            dropdowns = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )

            if identifier >= len(dropdowns):
                raise IndexError(
                    f"Hanya ada {len(dropdowns)} dropdown, index {identifier} tidak tersedia."
                )

            dropdown_el = wait.until(EC.element_to_be_clickable(dropdowns[identifier]))
        elif by == "xpath":
            dropdown_el = wait.until(
                EC.element_to_be_clickable((By.XPATH, str(identifier)))
            )
        else:
            raise ValueError("Parameter 'by' harus 'id', 'index', atau 'xpath'.")

        if value == "__reset__":
            if dropdown_el.tag_name.lower() == "select":
                select = Select(dropdown_el)
                select.select_by_index(0)
            else:
                dropdown_el.click()
                option_el = dropdown_el.find_element(By.XPATH, ".//li[1]")
                option_el.click()
            return

        if dropdown_el.tag_name.lower() == "select":
            select = Select(dropdown_el)
            select.select_by_value(value)
        else:
            dropdown_el.click()
            option_xpath = f".//*[text()='{value}' or @value='{value}']"
            option_el = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option_el.click()

    except Exception as e:
        raise Exception(
            f"Dropdown dengan {by}='{identifier}' tidak ditemukan atau tidak bisa dipilih: {e}"
        )

