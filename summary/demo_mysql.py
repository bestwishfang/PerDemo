# -*- coding: utf-8 -*-
# from gevent import monkey
#
# monkey.patch_all()
#
# import gevent
import pymysql
import threading

from queue import Queue

class MysqlManager(object):

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.initial()

    def initial(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database)
            self.cursor = self.conn.cursor()
        except pymysql.err.OperationalError as err:
            print(f'Connect to MySQL server failed!!! [Error] {err}')

    def query(self, table, query_option, option, value, limit_str=None):
        sql = f"select {query_option} from {table} where {option} in {value};"
        if limit_str:
            sql = f'{sql} {limit_str};'
        else:
            sql = f'{sql};'
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            return ret
        except Exception as err:
            print(f'Query Error: {err}\nSql: {sql}')

    def insert(self, table, options, values):
        sql = f"insert into {table} ({options}) values ({values});"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(f'Insert Error: {err}\nSql: {sql}')
            self.conn.rollback()

    def update(self, table, update_option, update_value, option, value):
        sql = f"update {table} set {update_option} = '{update_value}' where {option} = '{value}';"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(f'Update Error: {err}\nSql: {sql}')
            self.conn.rollback()

    def delete(self, table, delete_option, delete_value):
        sql = f"delete from {table} where {delete_option} = '{delete_value}';"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(f'Delete Error: {err}\nSql: {sql}')
            self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()


def task_update(queue_obj):
    sql_obj = queue_obj.get()
    sql_obj.update('person', 'id', 5, 'name', '匆匆')


def task_query(queue_obj):
    sql_obj = queue_obj.get()
    ret = sql_obj.query('good', '*', 'price', (10, 100))
    print(ret)


def main():
    queue_obj = Queue()
    sql_obj = MysqlManager(host='10.10.12.147',
                           port=3306,
                           user='root',
                           password='123456',
                           database='demo')
    queue_obj.put(sql_obj)
    queue_obj.put(sql_obj)
    # gevent.spawn(task_query)
    # gevent.spawn(task_update)

    t1 = threading.Thread(target=task_update, args=(queue_obj, ))
    t2 = threading.Thread(target=task_query, args=(queue_obj, ))
    t1.start()
    t2.start()

    pass


if __name__ == '__main__':

    main()
