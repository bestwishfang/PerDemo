# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class PatengxunPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               password='123456',
                               db='spiderwork')
        cursor = conn.cursor()

        sql = "insert into tengxun(title, source, url, release_time, content, engineer) values(%s, %s, %s, %s, %s, %s)"
        data = (item['title'], item['source'], item['url'], item['release_time'], item['content'], item['engineer'])
        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        return item
    
    
class PatongjiPipeline(object):
    def __init__(self):
        pass


    def process_item(self, item, spider):
        conn = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               password='123456',
                               db='spiderwork')
        cursor = conn.cursor()

        sql = "insert into tongjiarea(area_name, area_code) values(%s, %s)"
        data = (item['area_name'], item['area_code'])
        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        return item

    def close_spider(self):
        pass
