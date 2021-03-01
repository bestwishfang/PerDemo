# -*- coding: utf-8 -*-
import scrapy
import json

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'PersonTest.pipelines.DoubanPipeline': 300,}
    }
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/chart']

    def parse(self, response):
        # with open('dou.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        table_list = response.xpath('//div[@class="article"]/div[@class="indent"]//table')
        # print(type(table_list))  # <class 'list'>
        for table in table_list:
            # print(type(table), table)
            # break
            if table.xpath('.//div[@class="pl3"]').extract():
                print(table.xpath('.//div[@class="pl2"]').extract())
            else:
                print(table.xpath('.//div[@class="pl3"]').extract())
                print("now no ")
            break



"""
<class 'scrapy.selector.unified.Selector'>
"""