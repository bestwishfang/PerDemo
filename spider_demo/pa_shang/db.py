# 主要负责数据库相关存储
import pymysql
import redis

from settings import REDIS_HOST, REDIS_PORT


class DBManager(object):
    # 初始化方法
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1',
                                        port=3306,
                                        user='root',
                                        password='123456',
                                        db='spiderwork')
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(err)

    # 保存数据方法
    def save_item(self, item):
        # SQL语法
        sql = "insert into shangwubu(title, url, release_time) values(%s, %s, %s) on duplicate key update title=values(title), release_time=values(release_time);"
        # 准备数据
        data = (item.title, item.url, item.release_time)
        # 执行
        self.cursor.execute(sql, data)
        # 提交
        self.conn.commit()

    # 对象回收
    def __del__(self):
        self.cursor.close()
        self.conn.close()


# 非关系型数据库
class RedisManager(object):
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

    def save_item(self, item):
        data = {
            'title': item.title,
            'url': item.url,
            'release_time': item.release_time,
        }
        self.r.sadd(item.sign, str(data))
        # self.r.set(item.sign, str(data))
