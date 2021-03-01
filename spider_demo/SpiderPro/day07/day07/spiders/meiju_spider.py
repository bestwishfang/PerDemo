# -*- coding: utf-8 -*-
import json
import scrapy
from urllib.parse import urljoin

from day07.items import MeijuItem


class MeijuSpiderSpider(scrapy.Spider):
    name = 'meiju_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'day07.pipelines.MeijuPipeline': 300,}
    }
    allowed_domains = ['meijutt.com']
    start_urls = ['https://www.meijutt.com/alltop_hit.html']

    def parse(self, response):
        data = {}
        div_list = response.xpath('//div[@class="top-min"]')
        for div in div_list:
            print(type(div), div)
            break
            # type_name = div.xpath('./div[@class="tt fn-clear"]/h5/text()').extract()
            # new_type_name = type_name[0]
            # print(new_type_name)
            # data[new_type_name] = []
            # li_list = div.xpath('./ul/li')
            # for li in li_list:
            #     movie_info = {}
            #     movie_index = li.xpath('./div[@class="lasted-num fn-left"]/i/text()').extract()[0]
            #     movie_name = li.xpath('./h5/a/text()').extract()[0]
            #     href = li.xpath('./h5/a/@href').extract()[0]
            #     movie_href = urljoin(response.url, href)
            # 
            #     movie_score_int = li.xpath('./div[@class="lasted-time fn-right"]/strong/text()').extract()[0]
            #     movie_score_folat = li.xpath('./div[@class="lasted-time fn-right"]/span/text()').extract()[0]
            #     movie_score = movie_score_int + movie_score_folat
            #     
                # item 对象
                # meiju_item = MeijuItem()
                # meiju_item['name'] = movie_name
                # meiju_item['href'] = movie_href
                # meiju_item['index'] = movie_index
                # meiju_item['score'] = movie_score
                # meiju_item['types'] = new_type_name
                #
                # yield meiju_item
                # yield scrapy.Request(url=movie_href, callback=self.detail_parse)
                # scrapy.FormRequest
                # break

                # movie_info['index'] = movie_index
                # movie_info['name'] = movie_name
                # movie_info['href'] = movie_href
                # movie_info['score'] = movie_score
                # data[new_type_name].append(movie_info)
                # print(movie_index, movie_name, movie_href, movie_score)
            # break
        # with open('meiju.json', mode='w', encoding='utf-8') as fp:
        #     json.dump(data, fp, ensure_ascii=False, indent=4)


    def detail_parse(self, response):
        # with open('detail_one.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        new_name = response.xpath('//div[@class="o_r_contact"]/ul/li[3]/text()').extract()[0]
        print(new_name)








"""
<class 'scrapy.selector.unified.Selector'> 
<Selector xpath='//div[@class="top-min"]' data='<div class="top-min"><div class="tt f...'>
"""