# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Day09Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BossJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()  # 公司名称
    salary = scrapy.Field()  # 职位薪资
    job_name = scrapy.Field()  # 职位名称
    job_url = scrapy.Field()  # 职位链接

