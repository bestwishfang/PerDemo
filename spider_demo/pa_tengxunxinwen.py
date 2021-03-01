import re
import json
import gevent
import random
import pymysql
import requests
import threading
from queue import Queue


def conn_mysql():
    conn = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='123456',
                           db='spiderwork')
    cursor = conn.cursor()
    return conn, cursor


def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(15):
        ret += random.choice(string)
    return ret


def request_url(url):
    agent = random_str()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': agent,
    }
    response = requests.get(url,headers=headers)
    ret = response.text
    return ret


def worker(news):
    news_info = {}
    news_url = news['url']
    news_source = news['source']
    news_info['title'] = news['title']
    news_info['source'] = news_source
    news_info['url'] = news_url
    news_ret = request_url(news_url)
    pattern = re.compile(r'content: (\{.*?)id:', re.S)
    news_str = pattern.findall(news_ret)[0].strip()
    news_str = news_str.rsplit(',', 1)[0]
    news_dict = json.loads(news_str, encoding='utf-8')
    news_content = news_dict['cnt_html']
    news_content = re.sub(r'\<(.*?)\>', '', news_content)
    news_content = news_content.rsplit('▌', 1)[0]
    news_info['content'] = news_content
    news_info['release_time'] = news_dict['alt_time']
    news_info['engineer'] = 'fang'
    print(news_info)
    if lock.acquire():
        sql = "insert into tengxunew(title, source, url, release_time, content, engineer) values(%s, %s, %s, %s, %s, %s)"
        news_data = (news_info['title'], news_info['source'], news_info['url'], news_info['release_time'], news_info['content'], news_info['engineer'])
        conn.ping(reconnect=True)
        try:
            cursor.execute(sql, news_data)
            conn.commit()
        except Exception as err_msg:
            print(err_msg)
            conn.rollback()
        lock.release()

    data[news_source].append(news_info)


def task(q):
    while not q.empty():
        url = q.get()
        ret = request_url(url)
        ret_dict = json.loads(ret, encoding='utf-8')
        if ret_dict['data']:
            gevent_list = []
            for news in ret_dict['data']:
                g = gevent.spawn(worker, news)
                gevent_list.append(g)
            gevent.joinall(gevent_list)


def crawl():
    q = Queue()
    mid_dict = {
        '央视新闻': 58,
        '中国新闻网': 1124,
        '中国周刊': 1156,
        '央视网新闻': 5278151,
        '人民网': 1456,
        '新华社新闻': 10859191,
        '北青Qnews': 16314728,
        '环球网': 26082,
        '新京报': 26134,
        '观察者网': 5006122,
        '第一财经': 5178949,
        '北京青年报': 5081830,
        '界面新闻': 5564731,
        '21世纪经济报道': 1233,
        '中国新闻周刊': 5069188,
        '光明网': 5215397,
        '正义网': 5029544,
        '法制网': 5065699,
        '中国证券报': 1368,
        '证券时报网': 1755,
    }
    for key, mid in mid_dict.items():
        data[key] = []
        for page in range(10):
            url = 'https://pacaio.match.qq.com/om/mediaArticles?mid={}&num=30&page={}'.format(mid, page)
            q.put(url)
    threading_list = []
    for i in range(10):
        t = threading.Thread(target=task, args=(q, ))
        t.start()
        threading_list.append(t)

    for t in threading_list:
        t.join()

    # with open('tengxun.json', mode='w', encoding='utf-8') as fp:
    #     json.dump(data, fp, ensure_ascii=False, indent=4)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    data = {}
    conn, cursor = conn_mysql()
    lock = threading.Lock()
    crawl()
