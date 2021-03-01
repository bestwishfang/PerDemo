from selenium import webdriver


url = 'https://www.pearvideo.com/video_1613542'
driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.get(url)

with open('video_1613542.html', mode='w', encoding='utf-8') as fp:
    fp.write(driver.page_source)
driver.save_screenshot('video_1613542.png')