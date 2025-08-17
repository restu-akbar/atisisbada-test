import unittest
import os
from dotenv import load_dotenv
from components.button import button
from components.form_input import form_input
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.filter_nibar import filter_nibar
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from components.checkbox import checkbox
from components.dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from datetime import datetime, timedelta


class TC_PNBR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.wait, cls.url = create_driver()
        cls.driver.get(cls.url)
        load_dotenv()
        user = os.getenv("user")
        password = os.getenv("password")
        login_page = LoginPage(cls.driver)
        login_page.login(user, password)
        TC_PNBR.nibar = os.getenv("nibar")
        driver = cls.driver
        time.sleep(3)
        driver.get(f"{cls.url}pages.php?Pg=pengamananPeralatan")

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()


    def test_TC_PNBR_004(self, isedit=False): 
        print("test_TC_PNBR_004")
        time.sleep(1)
        filter_nibar(self.driver, TC_PNBR.nibar)
        time.sleep(1)
        checkbox(self.driver, identifier=1, by="index", table_selector="table.koptable")
        time.sleep(1)
        href_button(self.driver, "javascript:pengamananPeralatan.formBaru()")
        alert_expected = (
            "Nama Pemakai belum diisi!" if isedit else "Pemakai belum dipilih!"
        )
        time.sleep(2)
        save_get_alert(self.driver, alert_expected, "TC_PNBR_004")

    def test_TC_PNBR_005(self):
        driver = self.driver
        print("test_TC_PNBR_005")
        time.sleep(1)
        button(driver, By.ID, "fmnama_pemakai_button")
        time.sleep(1)
        checkbox(
            driver,
            identifier=1,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )
        time.sleep(1)
        driver.execute_script("PegawaiPilih.windowSave();")
        time.sleep(1)
        save_get_alert(driver, "Status Pemakai belum diisi!", "TC_PNBR_005")

    def test_TC_PNBR_006(self):
        driver = self.driver
        value = "5"
        Dropdown(driver, identifier="fmstatus_pemakai", value=value, by="id")
        time.sleep(1)
        if value != "5":
            print("test_TC_PNBR_007")
            print("----TC_PNBR_006 skipped---- ")
            save_get_alert(
                self.driver, "Nomor Identitas Pemakai belum diisi!", "TC_PNBR_007"
            )
        else:
            print("test_TC_PNBR_006")
            save_get_alert(
                self.driver, "Status Pemakai Lainnya belum diisi!", "TC_PNBR_006"
            )

    def test_TC_PNBR_007(self):
        driver = self.driver
        try:
            driver.switch_to.alert.accept()
        except Exception:
            pass
        current_value = driver.find_element(By.ID, "fmstatus_pemakai").get_attribute(
            "value"
        )

        if current_value != "5":
            self.skipTest('fmstatus_pemakai != "5" — TC_PNBR_007 di-skip')

        print("test_TC_PNBR_007")
        form_input(driver, By.ID, "fmstatus_pemakai_lainnya", "pegawai pembantu")
        time.sleep(1)
        save_get_alert(
            self.driver, "Nomor Identitas Pemakai belum diisi!", "TC_PNBR_007"
        )

    def test_TC_PNBR_008(self):
        driver = self.driver
        print("test_TC_PNBR_008")
        form_input(driver, By.ID, "fmno_ktp_pemakai", "12345678")
        time.sleep(1)
        save_get_alert(driver, "Alamat Pemakai belum diisi!", "TC_PNBR_008")
        pass

    def test_TC_PNBR_009(self):
        driver = self.driver
        print("test_TC_PNBR_009")
        form_input(driver, By.ID, "fmalamat_pemakai", "Alamat Testing")
        time.sleep(1)
        save_get_alert(driver, "Nomor BAST belum diisi!", "TC_PNBR_009")

    def test_TC_PNBR_010(self):
        driver = self.driver
        print("test_TC_PNBR_010")
        form_input(driver, By.ID, "fmno_bast", "08/bast/2025")
        time.sleep(1)
        save_get_alert(driver, "Tanggal BAST belum diisi!", "TC_PNBR_010")

    def test_TC_PNBR_011(self):
        driver = self.driver
        print("test_TC_PNBR_011")
        today = datetime.now().strftime("%d-%m-%Y")
        driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()
        driver.find_element(By.ID, "fmtgl_bast").send_keys(today)
        time.sleep(1)
        save_get_alert(driver, "Diinput Oleh belum diisi!", "TC_PNBR_011")

    def test_TC_PNBR_012(self):
        driver = self.driver
        print("test_TC_PNBR_012")
        Dropdown(driver, identifier="fmdiinput_oleh", value="1", by="id")
        time.sleep(1)
        save_get_alert(driver, "Diinput Nama belum dipilih!", "TC_PNBR_012")

    def test_TC_PNBR_013(self): 
        driver = self.driver
        print("test_TC_PNBR_013")
        button(driver, By.ID, "fmdiinput_nama_button")
        time.sleep(1)
        checkbox(
            driver,
            identifier=1,
            by="index",
            table_selector="#PegawaiPilih_cont_daftar > table",
        )
        time.sleep(1)
        driver.execute_script("PegawaiPilih.windowSave();")
        time.sleep(1)
        
        # Click second calendar icon 
        calendar_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#fmtgl_buku_tgl + img.ui-datepicker-trigger"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", calendar_icon)
        calendar_icon.click()
        time.sleep(3)
        button_calender = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-datepicker-div > table > tbody > tr:nth-child(4) > td:nth-child(6) > a"))
        )
        button_calender.click()
        time.sleep(5)

        driver.find_element(By.ID, "btSimpan").click() # ini seharusnya tdak bisa dan memberikan alert
        save_get_alert(driver, "Diinput Nama belum dipilih!", "TC_PNBR_012")


    # def test_TC_PNBR_014(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_014")
    #     next_day = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    #     time.sleep(1)
    #     driver.find_element(By.ID, "fmdiinput_nama_button").click()
    #     time.sleep(1)
    #     checkbox(
    #         driver,
    #         identifier=2,
    #         by="index",
    #         table_selector="#PegawaiPilih_cont_daftar > table",
    #     )
    #     time.sleep(1)

    #     pilih_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable(
    #             (
    #                 By.CSS_SELECTOR,
    #                 "#div_border > div:nth-child(3) > div > input[type=button]:nth-child(1)",
    #             )
    #         )
    #     )
    #     driver.execute_script("PegawaiPilih.windowSave();", pilih_button)

    #     time.sleep(1)
    #     driver.find_element(By.ID, "btSimpan").click()
    #     time.sleep(1)

    #     alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    #     alert_text = alert.text.strip()
    #     print(f"ℹ️ Alert text: {alert_text}")

    #     expected_text = f"Tanggal Transaksi Pengamanan tidak lebih kecil dari Tanggal BAST! ({next_day})"
    #     self.assertIn(
    #         expected_text, alert_text, f"Alert text mismatch, got: {alert_text}"
    #     )

    #     alert.accept()

    # def test_TC_PNBR_015(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_015")

    # def test_TC_PNBR_016(self):
    #     driver = self.driver
    #     day = (datetime.now() - timedelta(days=3)).strftime("%d-%m-%Y")
    #     print("test_TC_PNBR_016")

    #     time.sleep(1)
    #     driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click()
    #     time.sleep(1)
    #     driver.find_element(By.ID, "fmtgl_bast").clear()
    #     driver.find_element(By.ID, "fmtgl_bast").send_keys(day)

    #     time.sleep(1)
    #     driver.find_element(By.ID, "btSimpan").click()
    #     time.sleep(1)
    #     driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
    #     time.sleep(1)
    #     driver.execute_script("document.body.style.zoom='70%'")
    #     time.sleep(1)
    #     pass

    # def test_TC_PNBR_017(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_017")
    #     driver.get(f"{self.url}index.php?Pg=05&SPg=05&jns=tetap")
    #     time.sleep(1)
    #     checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
    #     driver.execute_script("document.body.style.zoom='80%'")
    #     time.sleep(1)
    #     pass

    # def test_TC_PNBR_018(self):
    #     driver = self.driver
    #     print("test_TC_PNBR_018")
    #     self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatan")
    #     time.sleep(1)
    #     filter_nibar(driver, self.nibar)
    #     driver.find_element(By.ID, "pengamananPeralatan_cb0").click()
    #     driver.find_element(By.ID, "fmMerk").send_keys("TOYOTA INNOVA E")
    #     time.sleep(1)
    #     driver.find_element(By.ID, "btTampil").click()
    #     time.sleep(1)

    #     checkbox(driver, identifier=1, by="index", table_selector="table.koptable")
    #     driver.find_element(By.CLASS_NAME, "toolbar").click()

    #     time.sleep(1)

    #     alert = Alert(driver)
    #     alert_text = alert.text
    #     print(f"ℹ️ Alert muncul: {alert_text}")
    #     self.assertEqual(
    #         alert_text,
    #         "Belum dilakukan pengembalian barang untuk pengguna/pemakai sebelumnya!",
    #         f"Teks alert tidak sesuai, dapat: {alert_text}",
    #     )
    #     alert.accept()
    #     time.sleep(1)

    def test_ZZZ_998(self):
        self.driver.get(f"{self.url}pages.php?Pg=pengamananPeralatanTrans")
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(1)
        self.driver.find_element(By.ID, "pengamananPeralatanTrans_cb0").click()
        time.sleep(1)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Batal").click()
        time.sleep(1)

        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(1)

        alert = Alert(self.driver)
        alert_text = alert.text
        print(f"ℹ️ Alert muncul: {alert_text}")
        alert.accept()
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()
