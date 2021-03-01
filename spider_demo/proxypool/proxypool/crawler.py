import json
from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        # print(attrs)
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count:页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    print(ip)
                    print(port)
                    yield ':'.join([ip, port])

    def crawl_ip3366(self):
        """
        获取ip3366的代理
        :return:
        """
        start_url = 'http://www.ip3366.net/?stype=1&page={}'
        urls = [start_url.format(page) for page in range(1, 4)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#list table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self):
        """
        获取kuaidaili
        :return:
        """
        for i in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('#list table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self):
        """
        获取xici
        :return:
        """
        for i in range(1, 4):
            start_url = 'https://www.xicidaili.com/nn/{}'.format(i)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr:first-child').siblings().items()
                for tr in trs:
                    ip = tr('td:nth-child(2)').text()
                    port = tr('td:nth-child(3)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        """
        获取data5u代理
        :return:
        """
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lis = doc('.l2').items()
            for li in lis:
                ip = li('span:nth-child(1)').text()
                port = li('span:nth-child(2)').text()
                yield ':'.join([ip, port])
