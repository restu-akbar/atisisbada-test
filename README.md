# atisisbada-test
Requirment
python 3.11,3.12
webdriver


Set up
0. Download web driver yang di inginkan simpan pada root folder (set up selenium more:https://selenium-python.readthedocs.io/installation.html)

1. python -m venv venv
2. venv\Scripts\activate (windows)
3. pip install -r requirements.txt


contoh untuk Running
# Running test yangtepat hanya satu saja (reccomended) 
python -m unittest tests.TC_PNEK.TC_PNEK

# Running seluruh test yang di temukan pada file nya
python -m unittest tests/TC_PNPE.py

