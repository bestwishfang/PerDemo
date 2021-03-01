# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Day07Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MeijuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    score = scrapy.Field()
    index = scrapy.Field()
    types = scrapy.Field()


class TengzhaoItem(scrapy.Item):
    
    title = scrapy.Field()
    location = scrapy.Field()
    last_update_time = scrapy.Field()
    url = scrapy.Field()
    requirement = scrapy.Field()
    responsibility = scrapy.Field()

