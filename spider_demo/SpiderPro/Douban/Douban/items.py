# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 书名
    url = scrapy.Field()  # 链接
    rate = scrapy.Field()  # 评分
    pinglun_nums = scrapy.Field()  # 评论人数
    img_url = scrapy.Field()  # 图片url
    
