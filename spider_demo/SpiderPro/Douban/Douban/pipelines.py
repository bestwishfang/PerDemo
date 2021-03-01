# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


class DoubanPipeline(object):
    def process_item(self, item, spider):
        # print(item['name'], item['url'])
        return item


# MongoDB 操作
class BookPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1',
                                          port=27017)
        self.db = self.client['book']

    def process_item(self, item, spider):
        # print(item['name'], item['url'])
        self.db['douban'].insert(dict(item))
        return item


# MySQL 操作
class NewBookPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    password='123456',
                                    db='spiderwork')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = ''
        data = ('', '')
        self.cursor.execute(sql, data)
        self.conn.commit()
        return item

    def close_spider(self):
        self.cursor.close()
        self.conn.close()
