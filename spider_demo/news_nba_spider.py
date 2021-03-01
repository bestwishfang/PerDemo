import re
import json
import gevent
import requests
import threading
from lxml import etree


def request_url(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    text = response.text
    tree = etree.HTML(text)
    return tree


def worker(news):
    news_info = {}
    news_name = news.xpath('.//h4/a/text()')[0]
    news_time = news.xpath('.//a[@class="time"]/@title')[0]
    news_source = news.xpath('.//span[@class="comeFrom"]/a/text()')[0]
    news_url = news.xpath('.//h4/a/@href')[0]
    news_info["新闻标题"] = news_name
    news_info["发布时间"] = news_time
    news_info["来源"] = news_source
    news_info["新闻链接"] = news_url

    sub_tree = request_url(news_url)
    news_art_list = sub_tree.xpath('//div[@class="voice-main"]//div[@class="artical-main-content"]/p/text()')
    news_article = ''.join([s.strip() for s in news_art_list])
    news_article = re.sub(r'虎扑(.*?)日讯 ', '', news_article)
    news_editor = sub_tree.xpath('//div[@class="voice-main"]//div[@class="artical-main-content"]/span/text()')
    news_editor = news_editor[0].strip()
    news_editor = re.search(r'\(编辑：(.*?)\)', news_editor).group(1)
    news_info["内容"] = news_article
    news_info["编辑"] = news_editor
    data[news_name] = news_info

    print("{} load over.".format(news_name))


def task(url):
    tree = request_url(url)
    news_list = tree.xpath('//div[@class="news-list"]/ul/li')
    gevent_list = []
    for news in news_list:
        g = gevent.spawn(worker, news)
        gevent_list.append(g)
    gevent.joinall(gevent_list)


def main():
    threading_list = []
    for i in range(1, 5):
        url = 'https://voice.hupu.com/nba/{}'.format(i)
        t = threading.Thread(target=task, args=(url,))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()

    json_str = json.dumps(data, ensure_ascii=False)
    with open('hupunba.txt', mode='w', encoding='utf-8') as f:
        f.write(json_str)
    # print(data)


if __name__ == '__main__':
    data = {}
    main()
