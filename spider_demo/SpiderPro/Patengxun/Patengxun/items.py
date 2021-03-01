# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PatengxunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    release_time = scrapy.Field()
    content = scrapy.Field()
    engineer = scrapy.Field()


class TongjiItem(scrapy.Item):
    area_name = scrapy.Field()
    area_code = scrapy.Field()

