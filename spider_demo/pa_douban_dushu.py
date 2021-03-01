#  爬取豆瓣读书   豆瓣读书搜索图书结果  数据是密文
import json
import threading
from selenium import webdriver


def task(url):
    driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(url)
    book_list = driver.find_elements_by_class_name('detail')
    for book in book_list:
        book_info = {}
        book_name = book.find_element_by_class_name('title-text').text

        book_str, price = book.find_element_by_xpath('.//div[@class="meta abstract"]').text.rsplit(r' / ', 1)
        book_str, date = book_str.rsplit(r' / ', 1)
        author, public = book_str.rsplit(r' / ', 1)

        book_info["书名"] = book_name.strip()
        book_info["作者/译者"] = author.strip()
        book_info["出版社"] = public.strip()
        book_info["出版时间"] = date.strip()
        book_info["价格"] = price.strip()

        data[book_info["书名"]] = book_info
        print('{} load over.'.format(book_info["书名"]))


def main(keyword):
    threading_list = []
    for i in range(3):  # 爬取前3页
        url = 'https://search.douban.com/book/subject_search?search_text={}&cat=1001&start={}'.format(keyword, 15 * i)
        t = threading.Thread(target=task, args=(url, ))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()

    with open('doubandushu.json', mode='w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data = {}
    keyword = input("请输入要搜索图书名称：").strip()
    main(keyword)