# -*- coding: utf-8 -*-
import time
import pymysql


def connect():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='123456',
                           database='demo',
                           )
    return conn


def main():
    conn = connect()
    cursor = conn.cursor()

    # sql = "select * from good;"
    # sql = "insert into good(name,num,price) values('鱿鱼',12,25);"
    sql = "select name, num, price from good where id in (1, 22);"

    cursor.close()  # cursor 很重要
    conn.close()
    time.sleep(2)
    try:
        if conn:
            print(f'Yes conn: {conn}')
        else:
            print(f'No conn: {conn}')
        conn.ping()
        cursor = conn.cursor()
    except Exception as err:
        print(err)
        conn = connect()
        cursor = conn.cursor()

    row = cursor.execute(sql)
    conn.commit()
    print(row)
    # print(type(cursor.fetchall()))  # tuple
    ret = cursor.fetchall()

    if ret:
        print("=================")
    else:
        print('-----------------------------')
    print(ret)
    print(type(ret))
    print(ret[0])
    print(type(ret[0]))
    # for x in cursor.fetchall():
    #     print(type(x))
    #     print(x)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
"""
SELECT * FROM mysql.general_log WHERE POSITION('7fc4cbcc2700603f6f4b1395a79a91e250a47cf37b5d2' in argument);
"""
