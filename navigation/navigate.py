import unittest
import os
from dotenv import load_dotenv
import time
from components.href_button import href_button

def to_peralatan_dan_mesin(driver):
    href_button(driver, "pages.php?Pg=pemeliharaan_daftar")
    href_button(driver, "pages.php?Pg=tanahInSertifikat")
    href_button(driver, "pages.php?Pg=pengamananPeralatan")
    pass