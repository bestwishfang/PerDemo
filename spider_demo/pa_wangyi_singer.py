# 爬取网页云音乐 所有歌手/团队名字 和 链接
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
    content = response.content.decode('utf-8')
    tree = etree.HTML(content)
    return tree


def worker(singer_type, type_href):
    url_root = 'https://music.163.com'
    singer_list = []
    for j in range(65, 91):  # 65 91
        singer_type_url_page = url_root + type_href + '&initial={}'.format(j)
        singer_tree = request_url(singer_type_url_page)
        singer_a_list = singer_tree.xpath(
            '//ul[@id="m-artist-box"]/li//a[@class="nm nm-icn f-thide s-fc0"] | //ul[@id="m-artist-box"]/li[@class="sml"]/a')
        for a in singer_a_list:
            singer_info = {}
            singer_info['url'] = url_root + a.xpath('./@href')[0].strip()
            singer_info['name'] = None
            if a.xpath('./text()'):
                singer_info['name'] = a.xpath('./text()')[0].strip()
            singer_list.append(singer_info)

    data[singer_type] = singer_list
    # print(data)


def task(singer_type_list, type_href_list):
    gevent_list = []
    for i in range(len(singer_type_list)):
        g = gevent.spawn(worker, *(singer_type_list[i], type_href_list[i]))
        gevent_list.append(g)
    gevent.joinall(gevent_list)


def main(tree):
    info_list = tree.xpath('//div[@class="blk"]')
    threading_list = []
    for info in info_list:
        singer_type_list = info.xpath('.//a/text()')
        type_href_list = info.xpath('.//a/@href')
        t = threading.Thread(target=task, args=(singer_type_list, type_href_list))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()

    # json_str = json.dumps(data, ensure_ascii=False)
    # with open('nsjjka.txt', mode='w', encoding='utf-8') as f:
    #     f.write(json_str)

    with open('wanyi_singer.json', mode='w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data = {}
    url = 'https://music.163.com/discover/artist'
    tree = request_url(url)
    main(tree)
