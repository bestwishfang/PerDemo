import time
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn = sqlalchemy.create_engine("mysql+pymysql://root:123456@127.0.0.1/demo")
base = declarative_base(conn)


class Good(base):
    __tablename__ = 'good'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(20))
    num = sqlalchemy.Column(sqlalchemy.INTEGER)
    price = sqlalchemy.Column(sqlalchemy.INTEGER)


class Person(base):
    __tablename__ = 'person'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(20))
    money = sqlalchemy.Column(sqlalchemy.INTEGER)


class Log(base):
    __tablename__ = 'log'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
    msg = sqlalchemy.Column(sqlalchemy.String(100))


class User(object):
    def __init__(self, name):
        self.name = name
        self.money = None

    def info(self):
        person_data = session.query(Person).filter(Person.name == self.name).first()
        print("{} 现有金额 {} 元".format(person_data.name, person_data.money))
        self.money = person_data.money
        # return self.money

    def buy(self):
        while True:
            print("===============商品信息===============")
            data = session.query(Good).all()
            for x in data:
                print("{} 现库存 {} 单价{} 元".format(x.name, x.num, x.price))
            good_name = input("请选择要购买的商品名称或者退出（Q/q)：").strip()
            if good_name.upper() == 'Q':
                break
            else:
                good = session.query(Good).filter(Good.name == good_name).first()
                # 1、用户资金与商品价格比较
                if self.money > good.price:
                    # 减用户现金
                    self.money -= good.price
                    person = session.query(Person).filter(Person.name == self.name).first()
                    person.money = self.money
                    session.merge(person)
                    # 2、判断商品库存
                    if good.num == 0:
                        session.rollback()
                        self.money += good.price
                    else:
                        # 减商品库存
                        good.num -= 1
                        session.merge(good)
                        # 写日志
                        session.add(Log(msg="{} 买了{}|{}".format(self.name, good.name, time.asctime())))
                        try:
                            session.commit()
                        except Exception as err_msg:
                            print(err_msg)
                            session.rollback()
                    print("{} 还有现金 {} 元".format(self.name, self.money))
                else:
                    print("{} 资金不足！余额{}元".format(self.name, self.money))


if __name__ == '__main__':
    # base.metadata.create_all(conn)

    Session = sessionmaker(bind=conn)
    session = Session()

    # session.add_all([
    #     Good(name='鞋', num=10, price=100),
    #     Good(name='碗', num=8, price=10),
    #     Good(name='苹果', num=20, price=12),
    #     Good(name='肥牛', num=100, price=30),
    #     Good(name='青岛大虾', num=6, price=40),
    #     Good(name='皮皮虾', num=15, price=32),
    #     Good(name='筷子', num=10, price=6),
    #     Person(name='李四', money=10000),
    #     Person(name='王五', money=10000),
    #     Person(name='马六', money=10000),
    #     Person(name='张三', money=10000),
    #     Person(name='赵四', money=10000),
    #     Person(name='王二', money=10000),
    # ])
    # session.commit()

    # 展示用户身份表
    data = session.query(Person).all()
    user_list = []
    for x in data:
        user_list.append(x.name)

    count = 6
    while count > 0:
        print(user_list)
        name = input("请选择用户身份：").strip()
        # 创建用户对象
        if name in user_list:
            user = User(name)
            user.info()
            # 用户买商品
            user.buy()
            break
        else:
            count -= 1
            print("输入用户身份有误！")
            print("您还有{} 次机会选择身份！".format(count))
