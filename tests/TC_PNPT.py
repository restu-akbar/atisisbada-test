import unittest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.button import button
from components.dropdown import Dropdown
from components.form_input import form_input
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.PM.save_get_alert import save_get_alert
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar_pembukuan
from helpers.logout_helper import logout
from helpers.print_result import print_result
from pages.login_page import LoginPage
import time


class TC_PNPT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        driver = cls.driver
        TC_PNPT.nibar = os.getenv("nibar")
        time.sleep(3)
        driver.get(f"{cls.url}index.php?Pg=05")
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        #         try:
        #             logout(cls.driver)
        #         except Exception as e:
        #             print(f"⚠️ Logout gagal: {e}")
        #         finally:
        #             cls.driver.quit()
        #
        cls.driver.quit()

    #
    def setUp(self):
        driver = self.driver
        if self._testMethodName not in "test_TC_PNPT_001":
            driver.get(f"{self.url}index.php?Pg=05")
            filter_nibar_pembukuan(self.driver, TC_PNPT.nibar)
            time.sleep(1)
            checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
            time.sleep(1)
            if self._testMethodName in "test_TC_PNPT_012":
                href_button(driver, "javascript:Reclass.reClass()")
            elif self._testMethodName in "test_TC_PNPT_013":
                href_button(driver, "javascript:MutasiBaru_ins.mutasibaru()")
                alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                time.sleep(1)
                alert.accept()
                time.sleep(1)
            else:
                href_button(driver, "javascript:updatebarang.formUpdate()")
            driver.switch_to.window(driver.window_handles[-1])

    @unittest.skip("untuk testing")
    def test_TC_PNPT_001(self):
        driver = self.driver
        filter_nibar_pembukuan(self.driver, TC_PNPT.nibar)
        time.sleep(1)
        checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(driver, "javascript:prosesEdit()")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("test_TC_PNPT_001")
        driver = self.driver
        element = driver.find_element(By.ID, "fmKET_KIB_B")
        current_value = element.get_attribute("value") or ""
        new_value = current_value + " untuk testing"
        form_input(driver, By.ID, "fmKET_KIB_B", new_value)
        time.sleep(1)
        save_get_alert(driver, "btsave", "Data telah di simpan", "TC_PNPT_001")
        driver.switch_to.window(driver.window_handles[0])

    @unittest.skip("untuk testing")
    def test_TC_PNPT_002(self):
        print("test_TC_PNPT_002")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "1")
        time.sleep(1)
        form_input(driver, By.ID, "hrg_baru", "150000000")
        time.sleep(1)
        form_input(driver, By.ID, "ket_koreksi", "penurunan nilai barang")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        self.alert_helper("TC_PNPT_002")

    @unittest.skip("untuk testing")
    def test_TC_PNPT_003(self):
        print("test_TC_PNPT_003")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "2")
        time.sleep(1)
        
        # biar lebih robust
        kondisi_text = driver.find_element(
            By.CSS_SELECTOR,
            "#areakondisi > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(3)"
        ).text.strip()
                
        if kondisi_text == "Baik":
            Dropdown(driver, "kondisi_baru", "2")
        else:
            Dropdown(driver, "kondisi_baru", "1")
            
        time.sleep(1)
        form_input(driver, By.ID, "ket_kondisi", "penurunan nilai barang")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT__003",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_004(self): # harus menggunakan 152429 akun sulthan
        print("test_TC_PNPT_004")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "3")
        time.sleep(1)
        form_input(driver, By.ID, "ketKapitalisasi", "penurunan nilai barang")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_005(self):
        print("test_TC_PNPT_005")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "5")
        time.sleep(1)
        button(driver, By.XPATH, "//input[@value='CARI BARANG']")
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "5241695")#akun sulthan
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT_005",with_button=False)
        
    @unittest.skip("untuk testing")
    def test_TC_PNPT_006(self):
        print("test_TC_PNPT_006")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "6")
        time.sleep(1)
        button(driver, By.CSS_SELECTOR, "#areagabung > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]:nth-child(2)")
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "16815")#akun sulthan
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing penggabungan")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected=f"NIBAR {TC_PNPT.nibar} masih dalam pengamanan penggunaan, harus pengembalian!",
            test_name="TC_PNPT_006",
            with_button=False
        )
        

    @unittest.skip("untuk testing")
    def test_TC_PNPT_007(self):
        print("test_TC_PNPT_007")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "07/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "8")
        time.sleep(1)
        button(driver, By.ID, "caribarang")
        time.sleep(1)
        form_input(driver, By.ID, "fmBARANG", "SUV")
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_updtKdBrg", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT_007",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_008(self):
        print("test_TC_PNPT_008")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "9")
        time.sleep(1)
        form_input(driver, By.ID, "ket_KoreksiKurang", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT_008",with_button=False)
        
    @unittest.skip("untuk testing")
    def test_TC_PNPT_009(self):
        print("test_TC_PNPT_009")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "6")
        time.sleep(1)
        button(driver, By.CSS_SELECTOR, "#areagabung > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(3) > input[type=button]:nth-child(2)")
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "16814")#Karena yang induk nya yang di jadikan target ini jadi terbalik env nibar = 16815(yang pengamanan)
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing penggabungan")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(
            driver,
            expected=f"Data berhasil di simpan !",
            test_name="TC_PNPT_009",
            with_button=False
        )
        
    @unittest.skip("untuk testing")
    def test_TC_PNPT_010(self):
        print("test_TC_PNPT_010")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "5")
        time.sleep(1)
        button(driver, By.XPATH, "//input[@value='CARI BARANG']")
        time.sleep(1)
        form_input(driver, By.ID, "IDBARANG", "16814")#akun sulthan mini bus dengan env nibar 24959000 ( sama kasus nya dengan 009, 16814 adalah induk nya jadi yang terhapus adalah 24959000)
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        form_input(driver, By.ID, "ket_gabung", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(driver,expected="Data berhasil di simpan !", test_name="TC_PNPT_010",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_011(self):
        print("test_TC_PNPT_011")
        driver = self.driver
        time.sleep(1)
        form_input(driver, By.ID, "no_bast", "05/BAST/2025")
        time.sleep(1)
        Dropdown(driver, "trans", "7")
        time.sleep(1)
        form_input(driver, By.ID, "fmHARGA_HAPUS", "2000000")
        time.sleep(1)
        form_input(driver, By.ID, "fmKET", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        time.sleep(1)
        save_get_alert(driver,expected="Data berhasil di simpan", test_name="TC_PNPT_011",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_012(self):
        print("test_TC_PNPT_012")
        driver = self.driver
        time.sleep(1)
        button(driver, By.ID, "caribarang")
        time.sleep(1)
        form_input(driver, By.ID, "fmBARANG", "SUV")
        time.sleep(1)
        button(driver, By.ID, "btTampil")
        time.sleep(1)
        button(driver, By.XPATH, '//table[@class="koptable"]/tbody/tr[1]/td[2]/a')
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT_012",with_button=False)

    @unittest.skip("untuk testing")
    def test_TC_PNPT_013(self):
        print("test_TC_PNPT_013")
        driver = self.driver
        Dropdown(driver, "fmSKPDBidang2", "25")
        time.sleep(1)
        Dropdown(driver, "fmSKPDskpd2", "01")
        time.sleep(1)
        Dropdown(driver, "fmSKPDUnit2", "0001")
        time.sleep(1)
        Dropdown(driver, "fmSKPDSubUnit2", "001")
        time.sleep(1)
        button(driver, By.ID, "BaruBAST")
        time.sleep(1)
        form_input(driver, By.ID, "no_ba", "08/BAST")
        time.sleep(1)
        button(driver, By.XPATH, '//input[@value="Simpan"]')
        time.sleep(1)
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        time.sleep(1)
        alert.accept()
        time.sleep(1)
        form_input(driver, By.ID, "ket", "testing")
        time.sleep(1)
        button(driver, By.ID, "btsave")
        save_get_alert(driver,expected="Barang masih dalam pengamanan penggunaan, harus pengembalian!", test_name="TC_PNPT_013",with_button=False)

    def alert_helper(self, testCase):
        try:
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            actual = alert is not None
            if alert.text == "Data berhasil di simpan":
                actual = False
            print_result(actual, True, testCase)
            alert.accept()
        except TimeoutException:
            self.fail("[❌] Alert tidak muncul dalam 10 detik")


if __name__ == "__main__":
    unittest.main()
