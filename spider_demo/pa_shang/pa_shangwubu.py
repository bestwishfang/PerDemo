import time
import requests
from lxml import etree
from urllib.parse import urljoin
from datetime import datetime

from models import News
from db import DBManager, RedisManager
from settings import UPDATE_RATE
from common import hash_item


def request_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode('utf-8')
    return content


def first_obj(obj):
    if obj:
        return obj[0]
    else:
        return ''


def parse_content(base_url, content):
    # with open('one.html', mode='w', encoding='utf-8') as fp:
    #     fp.write(content)
    tree = etree.HTML(content)
    news_list = tree.xpath('//section[@class="f-mt20"]/ul/li')

    # 创建一个数据库对象
    # db = DBManager()
    r = RedisManager()
    for news in news_list:
        title = news.xpath('./a/text()')
        url = news.xpath('./a/@href')
        release_time = news.xpath('./span/text()')
        if title and url and release_time:
            url = urljoin(base_url, url[0])

            str_obj = title[0] + url + release_time[0]
            sign = hash_item(str_obj)
            # print(type(sign), sign)

            # 利用数据模型创建数据对象，给对象属性赋值
            item = News(title[0], url, release_time[0])
            item.sign = sign
            r.save_item(item)

            # 存储数据
            # db.save_item(item)

            # print(title[0], url, release_time[0])
            # release_time = release_time[0]
            # release_time_stamp = release_time.timestamp()
            # print(release_time_stamp)
            # news_time = time.mktime(time.strptime(release_time,'%Y-%m-%d %H:%M:%S'))
            # print(type(release_time), release_time)
            # print(type(news_time), news_time)  # <class 'float'> 1572315417.0
            # print(type(url), url)
            # print(type(title[0]), title[0])  # <class 'lxml.etree._ElementUnicodeResult'>


if __name__ == '__main__':
    for page in range(1, UPDATE_RATE + 1,1):
        if page==1:
            page = ''
        url = 'http://www.mofcom.gov.cn/article/ae/ai/?{}'.format(page)
        print(url)
        content = request_content(url)
        parse_content(url, content)




