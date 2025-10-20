from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By

def button(driver, by, locator, timeout=10, retry_if_intercepted=True):
    wait = WebDriverWait(driver, timeout)
    
    try:
        element = wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()
    
    except ElementClickInterceptedException:
        if retry_if_intercepted:
            print("[INFO] Element intercepted, trying to find next matching element...")
            
            # cari semua elemen yang cocok dengan locator
            elements = driver.find_elements(by, locator)
            
            for i, el in enumerate(elements):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    el.click()
                    print(f"[INFO] Clicked alternative button index={i}")
                    return
                except ElementClickInterceptedException:
                    continue  # lanjut ke elemen berikutnya
            
            print("[WARN] All matching buttons were intercepted, none clickable.")
        else:
            print("[ERROR] Element was intercepted and retry disabled.")
    
    except TimeoutException:
        print(f"[ERROR] Timeout waiting for element {locator}")
