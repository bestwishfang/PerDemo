import json
import threading
from selenium import webdriver


def task(url):
    driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(url)
    loupan_list = driver.find_elements_by_xpath('//ul[@class="resblock-list-wrapper"]/li')
    for loupan in loupan_list:
        loupan_info = {}
        loupan_name = loupan.find_element_by_xpath('.//a[@class="name "]').text.strip()
        loupan_img_url = loupan.find_element_by_class_name('lj-lazy').get_attribute('data-original')
        loupan_type = loupan.find_element_by_xpath('.//span[@class="resblock-type"]').text.strip()
        loupan_location = loupan.find_element_by_xpath('.//div[@class="resblock-location"]/span[1]').text.strip()
        loupan_area = loupan.find_element_by_xpath('.//div[@class="resblock-area"]/span').text.strip()
        loupan_avg_price = loupan.find_element_by_xpath('.//div[@class="main-price"]/span[1]').text.strip() + \
                           loupan.find_element_by_xpath('.//div[@class="main-price"]/span[2]').text.strip()
        # loupan_total_price = loupan.find_element_by_xpath('.//div[@class="resblock-price"]/div[@class="second"]').text.strip()
        loupan_info["楼盘名称"] = loupan_name
        loupan_info["楼盘图片链接"] = loupan_img_url
        loupan_info["类型"] = loupan_type
        loupan_info["所在区域"] = loupan_location
        loupan_info["户型建筑面积"] = loupan_area
        loupan_info["均价"] = loupan_avg_price

        data.append(loupan_info)
        print('{} load over.'.format(loupan_name))


def main():
    threading_list = []
    for i in range(1, 3):
        url = 'https://bj.fang.lianjia.com/loupan/pg{}/'.format(i)
        t = threading.Thread(target=task, args=(url,))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()

    with open('lianjia.txt', mode='w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)


if __name__ == '__main__':
    data = []
    main()
