# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider

# 在爬虫文件中需要修改3处


# class MaoyanSpider(scrapy.Spider):
#     name = 'maoyan'
#     allowed_domains = ['maoyan.com']
#     start_urls = ['http://maoyan.com/']
#
#     def parse(self, response):
#         pass

class MaoyanSpider(RedisSpider):
    name = 'maoyan'
    # allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']
    redis_key = 'maoyan:start_urls'

    def parse(self, response):
        # 在此处做数据解析
        print('spider url:', response.url)
        with open('task.txt', mode='a', encoding='utf-8') as fp:
            fp.write(response.url + '\n')
