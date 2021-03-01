import time
from selenium import webdriver

url = 'file:///E:/GoogleDownload/Python%E5%BC%80%E5%8F%91%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98.html'
driver = webdriver.PhantomJS(executable_path=r'D:/phantomjs-2.1.1-windows/bin/phantomjs.exe')

driver.maximize_window()
driver.get(url)  # Load page
time.sleep(15)
driver.save_screenshot('./per_info.png')
driver.close()
