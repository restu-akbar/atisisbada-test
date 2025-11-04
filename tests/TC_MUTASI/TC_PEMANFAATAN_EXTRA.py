import unittest
from datetime import datetime, date
from zoneinfo import ZoneInfo
import calendar
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)

import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from components.dropdown import Dropdown
from components.form_input import form_input,get_value_form,parse_currency
from components.button import button
from components.checkbox import checkbox
from components.href_button import href_button
from helpers.driver_setup import create_driver
from helpers.logout_helper import logout
from helpers.PM.save_get_alert import save_get_alert
from helpers.print_result import print_result
from helpers.filter_nibar import filter_nibar_pembukuan,filter_pengamanan

from selenium.webdriver.common.alert import Alert
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC

#python -m unittest tests.TC_MUTASI.TC_PEMANFAATAN_EXTRA
#python -m unittest tests.TC_MUTASI.TC_PEMANFAATAN_EXTRA -k test_TC_PEMANFAATAN_EXTRA_003
class TC_PEMANFAATAN_EXTRA(unittest.TestCase):
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
        TC_PEMANFAATAN_EXTRA.nibar = os.getenv("nibar")
        time.sleep(2)
        driver.get(f"{cls.url}pages.php?Pg=gantirugi")
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        try:
            logout(cls.driver)
        except Exception as e:
            print(f"⚠️ Logout gagal: {e}")
        finally:
            cls.driver.quit()
        
        # cls.driver.quit()
        
    def switch_to_main_window(driver):
        """Force switch to the first (main) window."""
        try:
            main = driver.window_handles[0]
            driver.switch_to.window(main)
        except Exception as e:
            print(f"[⚠️] Tidak bisa switch ke main window: {e}")

    def tearDown(self):
        d = getattr(self, "driver", None)
        if not d or not getattr(d, "session_id", None):
            return

        try:
            handles = d.window_handles
            if len(handles) > 1:
                # close only if still valid
                current = d.current_window_handle
                target = next((h for h in reversed(handles) if h != current), None)
                try:
                    d.close()
                except Exception as e:
                    print(f"[⚠️] Gagal close window: {e}")
                if target in d.window_handles:
                    d.switch_to.window(target)
            # if only 1 handle → do nothing, keep it open for next test
        except Exception as e:
            print(f"[⚠️] Gagal menutup tab atau berpindah: {e}")

    @unittest.skip("Pemanfaatan Pinjam_Pakai")
    def test_TC_PEMANFAATAN_EXTRA_001(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_001"
        print(tc)
        print("Pinjam Pakai")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_delete")
        time.sleep(2)
        
    @unittest.skip("Pemanfaatan Sewa")
    def test_TC_PEMANFAATAN_EXTRA_002(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_002"
        print(tc)
        print("Sewa")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Sewa",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Sewa",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Sewa",test_case=tc+"_delete")
        time.sleep(2)
        
    @unittest.skip("Pemanfaatan Kerjasama_Pemanfaatan")
    def test_TC_PEMANFAATAN_EXTRA_003(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_003"
        print(tc)
        print("Kerjasama_Pemanfaatan")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_delete")
        time.sleep(2)
        
    @unittest.skip("Pemanfaatan Bangun_Guna_Serah")
    def test_TC_PEMANFAATAN_EXTRA_004(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_004"
        print(tc)
        print("Bangun_Guna_Serah")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_delete")
        time.sleep(2)
        
    @unittest.skip("Pemanfaatan Bangun_Serah_Guna")
    def test_TC_PEMANFAATAN_EXTRA_005(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_005"
        print(tc)
        print("Bangun_Serah_Guna")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_delete")
        time.sleep(2)
        
    @unittest.skip("Pemanfaatan Kerjasama_Penyediaan_Infrastruktur")
    def test_TC_PEMANFAATAN_EXTRA_006(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_006"
        print(tc)
        print("Kerjasama_Penyediaan_Infrastruktur")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Pinjam Pakai") #nibar 152430
    def test_TC_PEMANFAATAN_EXTRA_007(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_007"
        print(tc)
        print("Pinjam Pakai")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Pinjam_Pakai",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Sewa")
    def test_TC_PEMANFAATAN_EXTRA_008(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_008"
        print(tc)
        print("Sewa")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Sewa",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Sewa",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Sewa",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Kerjasama_Pemanfaatan")
    def test_TC_PEMANFAATAN_EXTRA_009(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_009"
        print(tc)
        print("Kerjasama_Pemanfaatan")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Kerjasama_Pemanfaatan",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Bangun_Guna_Serah")
    def test_TC_PEMANFAATAN_EXTRA_010(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_010"
        print(tc)
        print("Bangun_Guna_Serah")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Bangun_Guna_Serah",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Bangun_Serah_Guna")
    def test_TC_PEMANFAATAN_EXTRA_011(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_011"
        print(tc)
        print("Bangun_Serah_Guna")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Bangun_Serah_Guna",test_case=tc+"_delete")
        time.sleep(2)
        
    # @unittest.skip("Pemanfaatan Kerjasama_Penyediaan_Infrastruktur")
    def test_TC_PEMANFAATAN_EXTRA_012(self):
        tc = "test_TC_PEMANFAATAN_EXTRA_012"
        print(tc)
        print("Kerjasama_Penyediaan_Infrastruktur")
        buatPemanfaatan(self.driver,self.url, self.nibar,is_create=True, jangka_waktu="5",tipe_aset="Aset_Lainnya", bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_create")
        editPemanfaatan(self.driver,self.url, self.nibar,is_create=False, jangka_waktu="3",bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_edit")
        hapusPemanfaatan(self.driver,self.url,self.nibar, bentuk_pemanfaatan="Kerjasama_Penyediaan_Infrastruktur",test_case=tc+"_delete")
        time.sleep(2)
        
        

def buatPemanfaatan(driver,url,nibar, is_create=True, jangka_waktu="5",tipe_aset="Aset_Tetap", bentuk_pemanfaatan="Sewa",test_case="unknown"):
    print("Buat Pemanfaatan:", bentuk_pemanfaatan)
    
    TIPE_ASET_PATH = {
        "Aset_Tetap": "index.php?Pg=05&SPg=03&jns=tetap",
        "Aset_Lainnya": "index.php?Pg=05&SPg=03&jns=lain",
    }

    # default ke aset tetap
    path = TIPE_ASET_PATH.get(tipe_aset, "index.php?Pg=05&SPg=03&jns=tetap")
    driver.get(f"{url}{path}")# Default https://t3st.atisisbada.id/index.php?Pg=05&SPg=03&jns=tetap
    
    filter_nibar_pembukuan(driver,nibar)
    time.sleep(1)
    checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
    href_button(driver, "javascript:pemanfaatanV2.formMulti()")
    
    # Look Up Table
    BENTUK_OPTIONS = {
        "Pinjam_Pakai": "1",
        "Sewa": "2",
        "Kerjasama_Pemanfaatan": "3",
        "Bangun_Guna_Serah": "4",
        "Bangun_Serah_Guna": "5",
        "Kerjasama_Penyediaan_Infrastruktur": "6"
    }
    
    today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
    tgl_str = f"{today.day}"  # contoh: "07"
    bln_str = f"{today.month:02d}"  # contoh: "09"
    thn_str = str(today.year)  # contoh: "2025"

    end_dt = add_one_month_safe(today)
    end_tgl_str = f"{end_dt.day}"
    end_bln_str = f"{end_dt.month:02d}"
    end_thn_str = str(end_dt.year)

    Dropdown(driver, "fmTANGGALPEMANFAATAN_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_thn", thn_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmJANGKAWAKTU", jangka_waktu)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_tgl", end_tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmTANGGALPEMANFAATAN_akhir_thn", end_thn_str)
    time.sleep(1)
    
    if is_create:
        value = BENTUK_OPTIONS.get(bentuk_pemanfaatan, "2")  # default nya "Sewa"
        Dropdown(driver, "fmBENTUKPEMANFAATAN", value)
        form_input(driver,By.ID,"fmKET", "auto testing create " + bentuk_pemanfaatan)
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        
        save_get_alert(
            driver,
            expected="Pemanfaatan 1 data Sukses",
            with_button=False,
            test_name=test_case,
        )
    else:
        button(driver, By.XPATH, "//input[@value='Simpan']")
        
def editPemanfaatan(driver,url,nibar, is_create=False, jangka_waktu="5", bentuk_pemanfaatan="Sewa",test_case="unknown"):
    print("edit Pemanfaatan:", bentuk_pemanfaatan)
    
    TIPE_PEMANFAATAN_PATH = {
        "Pinjam_Pakai": "index.php?Pg=06&bentukmanfaat=1",
        "Sewa": "index.php?Pg=06&bentukmanfaat=2",
        "Kerjasama_Pemanfaatan": "index.php?Pg=06&bentukmanfaat=3",
        "Bangun_Guna_Serah": "index.php?Pg=06&bentukmanfaat=4",
        "Bangun_Serah_Guna": "index.php?Pg=06&bentukmanfaat=5",
        "Kerjasama_Penyediaan_Infrastruktur": "index.php?Pg=06&bentukmanfaat=6"
    }

    # default ke aset tetap
    path = TIPE_PEMANFAATAN_PATH.get(bentuk_pemanfaatan, "index.php?Pg=05&SPg=03&jns=tetap")
    driver.get(f"{url}{path}")
    Dropdown(driver, "fmidberakhir", 0)
    filter_pengamanan(driver, nibar or "", "fmid")
    
    time.sleep(1)
    checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
    href_button(driver, "javascript:PemanfaatForm.Edit()")
    
    today = datetime.now(ZoneInfo("Asia/Jakarta")).date()
    tgl_str = f"{today.day}"  # contoh: "07"
    bln_str = f"{today.month:02d}"  # contoh: "09"
    thn_str = str(today.year)  # contoh: "2025"

    end_dt = add_one_month_safe(today)
    end_tgl_str = f"{end_dt.day}"
    end_bln_str = f"{end_dt.month:02d}"
    end_thn_str = str(end_dt.year)

    Dropdown(driver, "fmTANGGALPEMANFAATAN_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_tgl", tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_bln", bln_str)
    time.sleep(1)
    Dropdown(driver, "fmSURATTANGGAL_thn", thn_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmJANGKAWAKTU", jangka_waktu)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_tgl", end_tgl_str)
    time.sleep(1)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    Dropdown(driver, "fmTANGGALPEMANFAATAN_akhir_bln", end_bln_str)
    time.sleep(1)
    form_input(driver, By.ID, "fmTANGGALPEMANFAATAN_akhir_thn", end_thn_str)
    time.sleep(1)
    
    form_input(driver,By.ID,"fmKET", "auto testing edit " + bentuk_pemanfaatan)
    
    if is_create:
        
        time.sleep(1)
        button(driver, By.ID, "btSimpan")
        print_result(True, True, test_case)
    else:
        button(driver, By.XPATH, "//input[@value='Simpan']")
        save_get_alert(
            driver,
            expected="Sukses Simpan Data",
            with_button=False,
            test_name=test_case,
        )
        
def hapusPemanfaatan(driver,url,nibar, bentuk_pemanfaatan="Sewa",test_case="unknown"):
    print("Hapus Pemanfaatan:", bentuk_pemanfaatan)
    
    TIPE_PEMANFAATAN_PATH = {
        "Pinjam_Pakai": "index.php?Pg=06&bentukmanfaat=1",
        "Sewa": "index.php?Pg=06&bentukmanfaat=2",
        "Kerjasama_Pemanfaatan": "index.php?Pg=06&bentukmanfaat=3",
        "Bangun_Guna_Serah": "index.php?Pg=06&bentukmanfaat=4",
        "Bangun_Serah_Guna": "index.php?Pg=06&bentukmanfaat=5",
        "Kerjasama_Penyediaan_Infrastruktur": "index.php?Pg=06&bentukmanfaat=6"
    }

    # default ke aset tetap
    path = TIPE_PEMANFAATAN_PATH.get(bentuk_pemanfaatan, "index.php?Pg=05&SPg=03&jns=tetap")
    driver.get(f"{url}{path}")
    time.sleep(1)
    
    Dropdown(driver, "fmidberakhir", 0)
    filter_pengamanan(driver, nibar or "", "fmid")
    
    time.sleep(1)
    checkbox(driver, identifier=0, by="index", table_selector="table.koptable")
    href_button(driver, "PemanfaatHapus.Hapus()")
    
    time.sleep(3)
    save_get_alert(
        driver,
        expected="Yakin 1 data akan di hapus?",
        with_button=False,
        test_name=test_case,
    )

def get_alert_text(self, timeout=5, auto_accept=True):
        time.sleep(3)
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            if auto_accept:
                alert.accept()
            return text
        except (TimeoutException, NoAlertPresentException):
            return None
        except Exception:
            return None
        
def add_one_month_safe(dt: date) -> date:
    y, m = dt.year, dt.month + 1
    if m == 13:
        y, m = y + 1, 1
    last_day_next = calendar.monthrange(y, m)[1]
    d = min(dt.day, last_day_next)
    return date(y, m, d)

if __name__ == "__main__":
    unittest.main()
    
    
