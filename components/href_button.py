from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _xpath_literal(s: str) -> str:
    """
    Buat literal XPath aman untuk string `s`.
    - Kalau tidak ada ' -> pakai '...'
    - Kalau tidak ada " -> pakai "..."
    - Kalau ada keduanya -> pakai concat('a',"'",'b',...)
    """
    if "'" not in s:
        return f"'{s}'"
    if '"' not in s:
        return f'"{s}"'
    parts = s.split("'")
    tokens = []
    for i, part in enumerate(parts):
        if part:
            tokens.append(f"'{part}'")
        if i != len(parts) - 1:
            tokens.append('"\'"')
    return "concat(" + ", ".join(tokens) + ")"


def href_button(driver, href_value=None, timeout=10, href_parts=None):
    wait = WebDriverWait(driver, timeout)
    candidates = set()
    if href_value:
        candidates.add(href_value)
        candidates.add(href_value.replace('"', "'"))
        candidates.add(href_value.replace("'", '"'))

    last_exc = None

    if href_parts:
        conds = " and ".join(
            [f"contains(@href, {_xpath_literal(p)})" for p in href_parts]
        )
        conds_onclick = " and ".join(
            [f"contains(@onclick, {_xpath_literal(p)})" for p in href_parts]
        )
        xpath_multi = f"//*[(self::a or self::button or @role='button') and ({conds} or {conds_onclick})]"
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_multi)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            try:
                el.click()
            except Exception:
                driver.execute_script("arguments[0].click();", el)
            return
        except Exception as e:
            last_exc = e

    for cand in candidates:
        lit = _xpath_literal(cand)
        xpath = (
            f"//a[contains(@href, {lit})] | "
            f"//*[(self::a or self::button or @role='button') and contains(@onclick, {lit})]"
        )
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            try:
                el.click()
            except Exception:
                driver.execute_script("arguments[0].click();", el)
            return
        except Exception as e:
            last_exc = e
            continue

    raise Exception(
        f"Tidak menemukan elemen dengan pola: href_value={href_value} href_parts={href_parts} "
        f"di @href/@onclick. Error terakhir: {last_exc}"
    )
