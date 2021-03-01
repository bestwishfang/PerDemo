import time
import random
import logging
import traceback
import requests
import threading
from lxml import etree
from queue import Queue
from urllib.parse import urljoin


def write_log(msg):
    file_handler = logging.FileHandler(filename='paBaiDuPython.log', mode='a', encoding='utf-8')
    stream_handler = logging.StreamHandler()
    log_format = '%(asctime)s-%(name)s【%(levelname)s】%(module)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S %p'
    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        handlers=[file_handler, stream_handler],
        level=logging.WARNING
    )
    logging.error(msg)


def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(15):
        ret += random.choice(string)
    return ret


def task(q):
    while not q.empty():
        try:
            page = q.get(block=False)
            pn = (page - 1) * 50
            url = 'http://tieba.baidu.com/f?kw=python&ie=utf-8&pn={}'.format(pn)
            agent = random_str()
            headers = {
                'User-Agent': agent,
            }
            content = requests.get(url, headers=headers, timeout=5).content.decode('utf-8')
            # print(url)
            parse_html(url, content)
        except Exception as err_msg:
            print(err_msg)
            msg = traceback.format_exc()
            new_msg = '\n' + msg
            write_log(new_msg)


def parse_html(url, content):
    tree = etree.HTML(content)
    li_list = tree.xpath('//li[@class=" j_thread_list clearfix"]')
    for li in li_list:
        title = li.xpath('.//a[@class="j_th_tit "]/text()')[0].strip()
        href = li.xpath('.//a[@class="j_th_tit "]/@href')[0].strip()
        full_href = urljoin(url, href)
        # print(type(full_href))
        info = title + ',' + full_href + '\n'
        with open('baiduPython.csv', mode='a+', encoding='utf-8') as fp:
            fp.write(info)
        print(title, full_href)


if __name__ == '__main__':
    start = time.time()
    q = Queue()
    for i in range(11, 21):
        q.put(i)

    threading_list = []
    for j in range(5):
        t = threading.Thread(target=task, args=(q, ))
        t.start()
        threading_list.append(t)

    for t in threading_list:
        t.join()
    print(time.time() - start)  # 24.158381700515747
    print("OK")

