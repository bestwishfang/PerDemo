# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider

from Shangwubu.items import ShangwubuItem


class RichangSpider(RedisSpider):
    name = 'richang'
    redis_key = 'shangwubu:start_urls'
    # allowed_domains = ['mofcom.gov.cn']
    # start_urls = ['http://www.mofcom.gov.cn/article/ae/ai/?']

    def parse(self, response):
        # with open('one.html', mode='wb') as fp:
        #     fp.write(response.body)
        news_list = response.xpath('//section[@class="f-mt20"]/ul/li')
        for news in news_list:
            title = news.xpath('./a/text()').extract()
            url = news.xpath('./a/@href').extract()
            release_time = news.xpath('./span/text()').extract()
            if title and url and release_time:
                url = urljoin(response.url, url[0])
                item = ShangwubuItem()
                item['title'] = title[0]
                item['url'] = url
                item['release_time'] = release_time[0]
                yield scrapy.Request(url=url, callback=self.detail_parse, meta={'data': item})

    def detail_parse(self, response):
        # with open('two.html', mode='wb') as fp:
        #     fp.write(response.body)

        # p_source = response.xpath('//p[@id="arsource"]')
        # atype = p_source.xpath('./span[@class="u-atype"]/text()').extract()
        # print(atype)
        con_list = response.xpath('//div[@id="zoom"]//p[@style="text-indent: 2em;"]')
        content = []
        for con in con_list:
            p_text = con.xpath('./text()').extract()
            if p_text:
                content.append(p_text[0].strip())
        item = response.meta['data']
        item['content'] = ''.join(content)
        yield item
