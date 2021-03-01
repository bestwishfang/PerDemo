# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShangwubuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    release_time = scrapy.Field()
    # source = scrapy.Field()
    # atype = scrapy.Field()
    # contype = scrapy.Field()
    content = scrapy.Field()