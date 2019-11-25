"""
li = [1, 34, 56, 78, 34, 23, 34, 56]
new_list = [x for x in li if li.count(x) == 1]
print(new_list)
"""
import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       password='123456',
                       database='demo',
                       )
cursor = conn.cursor()

# sql = "select * from good;"
# sql = "insert into good(name,num,price) values('鱿鱼',12,25);"
sql = "select name, num, price from good;"
row = cursor.execute(sql)
conn.commit()

print(row)
# print(type(cursor.fetchall()))  # tuple
for x in cursor.fetchall():
    print(x)

cursor.close()
conn.close()
