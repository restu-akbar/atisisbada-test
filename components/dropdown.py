from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def Dropdown(
    driver, identifier, value=None, by="id", timeout=10, dropdown_selector=None
):
    """
    Memilih opsi atau mengambil nilai default dari elemen dropdown (<select> atau kustom).

    Args:
        driver: Objek Selenium WebDriver.
        identifier: Pengenal elemen dropdown (ID, indeks, atau XPath).
        value:
            - None -> ambil nilai default
            - "__reset__" -> reset ke opsi pertama
            - int -> pilih berdasarkan index
            - str -> pilih berdasarkan atribut `value` atau teks
        by: Metode untuk menemukan elemen: "id", "index", atau "xpath".
        timeout: Waktu tunggu (detik).
        dropdown_selector: Pemilih CSS untuk `by="index"`.

    Returns:
        str or None: Nilai default jika `value=None`, None jika memilih opsi.
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

        # === Ambil default value ===
        if value is None:
            if dropdown_el.tag_name.lower() == "select":
                select = Select(dropdown_el)
                selected_option = select.first_selected_option
                return (
                    selected_option.get_attribute("value") if selected_option else None
                )
            else:
                raise Exception("Elemen bukan dropdown <select> standar.")

        # === Reset ke index 0 ===
        if value == "__reset__":
            if dropdown_el.tag_name.lower() == "select":
                Select(dropdown_el).select_by_index(0)
            else:
                dropdown_el.click()
                option_el = dropdown_el.find_element(By.XPATH, ".//li[1]")
                option_el.click()
            return None

        # === Pilih berdasarkan index ===
        if isinstance(value, int):
            if dropdown_el.tag_name.lower() == "select":
                Select(dropdown_el).select_by_index(value)
            else:
                dropdown_el.click()
                option_xpath = f".//li[{value + 1}]"  # karena li[1] = index 0
                option_el = wait.until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option_el.click()
            return None

        # === Pilih berdasarkan value/teks ===
        if dropdown_el.tag_name.lower() == "select":
            Select(dropdown_el).select_by_value(value)
        else:
            dropdown_el.click()
            option_xpath = f".//*[text()='{value}' or @value='{value}']"
            option_el = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option_el.click()

        return None

    except Exception as e:
        raise Exception(
            f"Dropdown dengan {by}='{identifier}' tidak ditemukan atau tidak bisa dipilih: {e}"
        )
