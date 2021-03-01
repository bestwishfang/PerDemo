# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class YiyaoItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class XiLieItem(scrapy.Item):
    taocan = scrapy.Field(serializer=list)
    pinglun_nums = scrapy.Field()
    seller = scrapy.Field()


class YiyaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()

    url = scrapy.Field()
    pic_url = scrapy.Field()
