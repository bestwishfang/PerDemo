# -*- coding: utf-8 -*-
import socket
import scrapy
import datetime
from SC.items import CarItem
from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider


host_ip = socket.gethostbyname(socket.gethostname())


class TaocheSpider(RedisSpider):
    name = 'taoche'
    # allowed_domains = ['taoche.com']
    # start_urls = []
    # with open(r'E:\Python_work\SpiderWork\SpiderPro\SC\city.txt', mode='r', encoding='utf-8') as fp:
    #     city_list = fp.readlines()
    #
    # with open(r'E:\Python_work\SpiderWork\SpiderPro\SC\pinpai.txt', mode='r', encoding='utf-8') as fp:
    #     pinpai_list = fp.readlines()
    #
    # city_list = list(set(city_list))
    # pinpai_list = list(set(pinpai_list))
    #
    # for city in city_list:
    #     for pinpai in pinpai_list:
    #         url = 'https://{}.taoche.com{}'.format(city.strip(), pinpai.strip())
    #         start_urls.append(url)
    redis_key = 'taoche:start_urls'

    def get_obj_list(self, obj_list):
        if obj_list:
            return obj_list[0]
        else:
            return ''

    def parse(self, response):
        
        print('spider url:', response.url)
        with open('task.txt', mode='a', encoding='utf-8') as fp:
            fp.write(response.url + '\n')
        
        total = response.xpath('//div[@class="paging-box the-pages"]/div/a[last()-1]/text()').extract()
        if self.get_obj_list(total):
            for i in range(1, int(self.get_obj_list(total)) + 1):
                page_url = response.url + '?page={}'.format(i)
                print(page_url)
                yield scrapy.Request(url=page_url, callback=self.list_parse, encoding='utf-8',
                                     dont_filter=True)
        elif response.xpath('//ul[@class="gongge_ul"]/li[@data-state="1"]'):
            print(response.url)
            yield scrapy.Request(url=response.url, callback=self.list_parse, encoding='utf-8',
                                 dont_filter=True)
        else:
            print("{}没有数据".format(response.url))

    def list_parse(self, response):
        # with open('car.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        li_list = response.xpath('//ul[@class="gongge_ul"]/li[@data-state="1"]')
        for li in li_list:
            title = li.xpath('./div[@class="gongge_main"]/a/span/text()').extract()
            href = li.xpath('./div[@class="gongge_main"]/a/@href').extract()
            if href:
                full_url = urljoin(response.url, href[0])
                year = li.xpath('./div[@class="gongge_main"]/p/i[1]/text()').extract()
                distance = li.xpath('./div[@class="gongge_main"]/p/i[2]/text()').extract()
                # location = li.xpath('./div[@class="gongge_main"]/p/i[3]/a/text()').extract()[0]
                price = li.xpath('./div[@class="gongge_main"]/div[@class="price"]/i[2]/text()').extract()

                ori_price = li.xpath('./div[@class="gongge_main"]/div[@class="price"]/i[3]/text()').extract()


                item = CarItem()
                item['c_title'] = self.get_obj_list(title)
                item['c_url'] = full_url
                item['c_year'] = self.get_obj_list(year)
                item['c_distance'] = self.get_obj_list(distance)
                # item['c_location'] = location
                item['c_ori_price'] = self.get_obj_list(ori_price).replace("原价", '')
                item['c_price'] = self.get_obj_list(price) + "万"
                item['c_crawl_time'] = datetime.datetime.now()

                # yield item
                # print(year)
                yield scrapy.Request(url=full_url, callback=self.detail_parse, meta={'data': item},
                                     encoding='utf-8', dont_filter=True)

    # 详情页的解析
    def detail_parse(self, response):
        item = response.meta['data']
        li_list = response.xpath('//div[@class="col-xs-6 parameter-configure-list"]/ul/li')
        # print(len(li_list))
        # 品牌， 型号
        pinpai_xinghao = li_list[0].xpath('./span/a/text()').extract()
        if pinpai_xinghao:
            pinpai, xinghao = pinpai_xinghao
        else:
            pinpai, xinghao = ('', '')
        # 车源所在地
        location = li_list[1].xpath('./span/text()').extract()
        # 发动机
        engine = li_list[2].xpath('./span/text()').extract()
        # 驱动方式
        driver = li_list[3].xpath('./span/text()').extract()
        # 车辆级别
        level = li_list[4].xpath('./span/a/text()').extract()
        # 排量
        pailiang = li_list[5].xpath('./span/a/text()').extract()
        # 油耗
        oil_wear = li_list[6].xpath('./span/text()').extract()
        # 长宽高
        length = li_list[7].xpath('./span/text()').extract()
        # 车身类型
        car_type = li_list[8].xpath('./span/text()').extract()
        # 后备箱容积
        volum = li_list[9].xpath('./span/text()').extract()
        # print(pinpai, xinghao, location, engine, driver, level)
        # print(pinpai, xinghao, location)
        item['c_location'] = self.get_obj_list(location)
        item['pinpai'] = pinpai
        item['xinghao'] = xinghao
        item['engine'] = self.get_obj_list(engine)
        item['driver'] = self.get_obj_list(driver)
        item['level'] = self.get_obj_list(level)
        item['pailiang'] = self.get_obj_list(pailiang)
        item['oil_wear'] = self.get_obj_list(oil_wear)
        item['length'] = self.get_obj_list(length)
        item['car_type'] = self.get_obj_list(car_type)
        item['volum'] = self.get_obj_list(volum)

        item['host_ip'] = host_ip
        yield item


"""
{
    "_id" : ObjectId("5db2be16df727717e42e83b5"),
    "c_title" : "奥迪A8L 2017款 45 TFSI quattro 豪华版",
    "c_url" : "https://www.taoche.com/buycar/b-dealerydg233703347t.html?source=2808",
    "c_year" : "2017年",
    "c_distance" : "3.95万公里",
    "c_location" : "北京",
    "c_ori_price" : "72.52万",
    "c_price" : "71.00万",
    "c_crawl_time" : ISODate("2019-10-25T17:19:18.048Z")
}
"""