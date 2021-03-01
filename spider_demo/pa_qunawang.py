import json
import gevent
import random
import requests
from lxml import etree
from concurrent.futures import thread, as_completed


proxies = { "http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080", }

def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(15):
        ret += random.choice(string)
    return ret


def request_url(url):
    agent = random_str()
    headers = {
        'User-Agent': agent,
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode('utf-8')
    tree = etree.HTML(content)
    return tree


def worker(scenery):
    scenery_info = {}
    scenery_name = scenery.xpath('.//h3/a/text()')[0].strip()
    scenery_level = scenery.xpath('.//div[@class="clrfix"]/span[@class="level"]/text()')
    scenery_redu = scenery.xpath('.//div[@class="clrfix"]//em/@title')[0].strip().split(': ', 1)[1]
    scenery_address = scenery.xpath('.//div[@class="sight_item_info"]/p/span/@title')[0].strip()
    scenery_desc = scenery.xpath('.//div[@class="sight_item_info"]/div[2]/text()')
    scenery_price = scenery.xpath('.//span[@class="sight_item_price"]/em/text()')
    scenery_sales = scenery.xpath('.//span[@class="hot_num"]/text()')
    img_url = scenery.xpath('.//div[@class="show loading"]/a/img/@data-original')[0].strip()
    if scenery_desc:
        scenery_desc = scenery_desc[0].strip()
    else:
        scenery_desc = ''

    if scenery_price:
        scenery_price = scenery_price[0].strip()
    else:
        scenery_price = ''

    if scenery_sales:
        scenery_sales = scenery_sales[0].strip()
    else:
        scenery_sales = ''

    if scenery_level:
        scenery_level = scenery_level[0].strip()
    else:
        scenery_level = "未标注"

    scenery_info["景点名称"] = scenery_name
    scenery_info["星级"] = scenery_level
    scenery_info["热度"] = scenery_redu
    scenery_info["地址"] = scenery_address
    scenery_info["简介"] = scenery_desc
    scenery_info["门票价格"] = scenery_price
    scenery_info["月销量"] = scenery_sales
    scenery_info["图片链接"] = img_url
    data.append(scenery_info)


def task(url):
    tree = request_url(url)
    scenery_list = tree.xpath('//div[@id="search-list"]/div')
    gevent_list = []
    for scenery in scenery_list:
        g = gevent.spawn(worker, scenery)
        gevent_list.append(g)
    gevent.joinall(gevent_list)
    return '{} load over.'.format(url)


def main():
    pool = thread.ThreadPoolExecutor(20)
    threading_list = []
    for i in range(1, 267):
        url = 'https://piao.qunar.com/ticket/list.htm?keyword=%E5%8C%97%E4%BA%AC&region=&from=mps_search_suggest&page={}'.format(i)
        t = pool.submit(task, url)
        threading_list.append(t)

    for future in as_completed(threading_list):
        ret = future.result()
        print(ret)

    with open('qunaer.json', mode='w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)


if __name__ == '__main__':
    data = []
    main()
