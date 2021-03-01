# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


# class ScPipeline(object):
#     def process_item(self, item, spider):
#         return item


class CarPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='10.10.14.245',
                                          port=27017)
        self.db = self.client['NewSC']
        
    def process_item(self, item, spider):
        self.db['cars'].insert(dict(item))
        return item