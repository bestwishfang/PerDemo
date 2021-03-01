# -*- coding: utf-8 -*-
import scrapy


class YaopinSpiderSpider(scrapy.Spider):
    name = 'yaopin_spider'
    allowed_domains = ['111.com.cn']
    start_urls = ['https://www.111.com.cn/search/search.action?keyWord=%25E6%2584%259F%25E5%2586%2592&gotoPage=1']

    def parse(self, response):
        with open('yaopin.html', mode='w', encoding='gbk') as fp:
            fp.write(response.text)

