# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql


# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# conn = sqlalchemy.create_engine("mysql+pymysql://root:123456@127.0.0.1/spiderwork")
# base = declarative_base(conn)
#
# class MeiJu(base):
#     __tablename__ = 'meiju'
#     id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
#     index = sqlalchemy.Column(sqlalchemy.INTEGER)
#     name = sqlalchemy.Column(sqlalchemy.String(64))
#     href = sqlalchemy.Column(sqlalchemy.String(100))
#     score = sqlalchemy.Column(sqlalchemy.FLOAT)
#     types = sqlalchemy.Column(sqlalchemy.String(32))
#
#
# Session = sessionmaker(bind=conn)
# session = Session()

# 将spider 传递过来的item 进行数据存储
class MeijuPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               password='123456',
                               db='spiderwork')
        cursor = conn.cursor()
        sql = "insert into meiju(m_index, name, href, score, m_type) values(%s, %s, %s, %s, %s)"
        data = (item['index'], item['name'], item['href'], item['score'], item['types'])
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()

        # print(type(item), item['name'])
        # with open('newmeiju.json', mode='a', encoding='utf-8') as fp:
        #     json.dump(dict(item), fp, ensure_ascii=False, indent=4)
        return item


class TengPipeline(object):
    def process_item(self, item, spider):
        # conn = pymysql.connect(host='127.0.0.1',
        #                        port=3306,
        #                        user='root',
        #                        password='123456',
        #                        db='spiderwork')
        # cursor = conn.cursor()
        with open('newteng.json', mode='a', encoding='utf-8') as fp:
            json.dump(dict(item), fp, ensure_ascii=False, indent=4)

        return item

