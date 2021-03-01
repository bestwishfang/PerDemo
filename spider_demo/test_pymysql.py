# 主要负责数据库相关存储
import pymysql


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
        sql = "insert into shangwubu(title, url, release_time) values(%s, %s, %s);"
        # 准备数据
        data = (item.title, item.url, item.release_time)
        # 执行
        self.cursor.execute(sql, data)
        # 提交
        self.conn.commit()

    # 查询数据
    def select_url(self):
        sql = "select release_time from shangwubu order by release_time desc;"
        self.cursor.execute(sql)
        # ret = self.cursor.fetchall()
        ret = self.cursor.fetchmany(4)
        return ret

    # 对象回收
    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = DBManager()
    ret = db.select_url()
    for r in ret:
        print(type(r), r)



"""
<class 'tuple'> (datetime.datetime(2019, 10, 29, 10, 16, 57),)
"""


