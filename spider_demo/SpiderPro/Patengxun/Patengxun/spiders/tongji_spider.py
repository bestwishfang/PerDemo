# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from Patengxun.items import TongjiItem


class TongjiSpiderSpider(scrapy.Spider):
    name = 'tongji_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'Patengxun.pipelines.PatongjiPipeline': 300,}
    }
    allowed_domains = ['www.stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']

    def parse(self, response):
        # with open('anhui.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        tr_list = response.xpath('//table[@class="provincetable"]//tr[@class="provincetr"]')
        # print(len(tr_list))  # 4
        for tr in tr_list:
            td_list = tr.xpath('./td')
            for td in td_list:
                name = td.xpath('./a/text()').extract()[0]
                href = td.xpath('./a/@href').extract()[0]
                detail_url = urljoin(response.url, href)

                yield scrapy.Request(url=detail_url, callback=self.detail_parse)
                # break
            # break

    def detail_parse(self, response):
        # with open('tongdetail.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        tj_item = TongjiItem()
        # print(response.url)
        table = response.xpath('''//table[@class='citytable'] | //table[@class="countyhead"] | //table[@class="towntable"] | //table[@class="villagetable"]''')
        tr_list = table.xpath("./tr[position()>1]")
        # tr_list = response.xpath('/HTML/BODY/TABLE[2]/TBODY/TR[1]/TD/TABLE/TBODY/TR[2]/TD/TABLE/TBODY/TR/TD')
        # print(len(tr_list))
        for tr in tr_list:
            if tr.xpath('.//a').extract():
                href = tr.xpath('./td[1]/a/@href').extract()[0]
                detail_url = urljoin(response.url, href)
                tj_item['area_code'] = tr.xpath('./td[1]/a/text()').extract()[0]
                tj_item['area_name'] = tr.xpath('./td[last()]/a/text()').extract()[0]
                yield tj_item
                yield scrapy.Request(url=detail_url, callback=self.detail_parse)
            else:
                tj_item['area_code'] = tr.xpath('./td[1]/text()').extract()[0]
                tj_item['area_name'] = tr.xpath('./td[last()]/text()').extract()[0]
                yield tj_item


"""
浏览器渲染出tbody
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]
/html/body/table[2]
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody  
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody
/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody
"""