# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo


class ShangwubuPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='10.10.14.245', port=27017)
        self.db = self.client['Shangwubu']

    def process_item(self, item, spider):
        data = dict(item)
        # with open('shangwubu.json', mode='a', encoding='utf-8') as fp:
        #     json.dump(data, fp, ensure_ascii=False, indent=4)
        self.db['richangnews'].insert(data)
        return item
