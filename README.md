# atisisbada-test

Requirement
python 3.11,3.12
webdriver

Set up 0. Download web driver yang di inginkan simpan pada root folder (set up selenium more:https://selenium-python.readthedocs.io/installation.html)

1. python -m venv venv
2. venv\Scripts\activate (windows)
3. pip install -r requirements.txt

contoh untuk Running

# Running semua fungsi test yang ada di satu file
python -m unittest tests.TC_PNEK.TC_PNEK

# Contoh running 1 fungsi test di salah satu file test
python -m unittest tests.TC_FLPK -k test_TC_FLPK_007 -k test_TC_FLPK_012

# Contoh running beberapa fungsi test sekaligus
python -m unittest tests.TC_FLPK -k test_TC_FLPK_007 -k test_TC_FLPK_012
