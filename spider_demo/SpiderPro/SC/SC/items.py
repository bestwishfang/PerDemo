# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    c_title = scrapy.Field()  # 标题
    c_location = scrapy.Field()  # 城市位置
    c_ori_price = scrapy.Field()  # 原价
    c_price = scrapy.Field()  # 现价
    c_year = scrapy.Field()  # 购买年份
    c_distance = scrapy.Field()  # 行驶距离
    c_crawl_time = scrapy.Field()  # 爬取时间
    c_url = scrapy.Field()

    # 详情页数据
    pinpai = scrapy.Field()
    xinghao = scrapy.Field()
    engine = scrapy.Field()
    driver = scrapy.Field()
    level = scrapy.Field()
    pailiang = scrapy.Field()
    oil_wear = scrapy.Field()
    length = scrapy.Field()
    car_type = scrapy.Field()
    volum = scrapy.Field()
    
    host_ip = scrapy.Field()
    
    

