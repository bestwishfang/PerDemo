# -*- coding: utf-8 -*-
import re
import scrapy
from Douban.items import BookItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'Douban.pipelines.BookPipeline': 300,},
        'DOWNLOADER_MIDDLEWARES': {'Douban.myMW.BookDownloaderMiddleware': 543,},
    }
    allowed_domains = ['douban.com']
    start_urls = ['https://search.douban.com/book/subject_search?search_text=python']

    def parse(self, response):
        # with open('book.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        book_list = response.xpath('//div[@class="item-root"]')
        for book in book_list:
            name = book.xpath('.//div[@class="title"]/a/text()').extract()[0]
            url = book.xpath('.//div[@class="title"]/a/@href').extract()[0]
            rate = book.xpath('./div//span[@class="rating_nums"]/text()').extract()[0]
            pinglun_nums = book.xpath('./div/div[2]/span[last()]/text()').extract()[0]
            nums = re.search(r'(\d+)', pinglun_nums).group(1)
            img_url = book.xpath('./a/img/@src').extract()[0]

            item = BookItem()
            item['name'] = name
            item['url'] = url
            item['rate'] = rate
            item['pinglun_nums'] = nums
            item['img_url'] = img_url
            yield item