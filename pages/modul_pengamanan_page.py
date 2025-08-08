from selenium.webdriver.common.by import By


class ModulPengamananPage:
    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self,page_name):
        return page_name in self.driver.page_source

    def click_transaksi_baru(self):
        self.driver.find_element(By.ID, "btn_tambah").click()
