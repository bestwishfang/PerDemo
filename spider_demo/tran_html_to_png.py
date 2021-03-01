import time
from selenium import webdriver


def tran_html_png(driver, url, save_file):
    """
    将 html 文件 保存为 png 图片
    :param driver: 浏览器引擎
    :param url: html 地址
    :param save_file: 要保存图片的文件名称
    :return: None
    """
    driver.maximize_window()
    driver.get(url)

    time.sleep(15)
    driver.save_screenshot(save_file)
    driver.close()


if __name__ == '__main__':

    url = 'file:///E:/Chrome DownLoads/seaborn_learning.html'
    # executable_path 浏览器引擎 路径
    driver = webdriver.PhantomJS(executable_path=r'D:/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    save_file = './seaborn_learning.png'
    tran_html_png(driver, url, save_file)

