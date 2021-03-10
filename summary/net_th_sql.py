import pymysql
import threading


class Db(object):
    def __init__(self, host=None, username=None, pwd=None, dbname=None):
        self.pool = {}
        self.host = host
        self.username = username
        self.pwd = pwd
        self.dbname = dbname

    def get_instance(self, ):
        name = threading.current_thread().name
        if name not in self.pool:
            conn = pymysql.connect(self.host, self.username, self.pwd, self.dbname)
            self.pool[name] = conn
        return self.pool[name]


class Test(object):
    def __init__(self):
        self.max_id = 10000
        self.start_id = 1
        self.db = Db('localhost', 'root', '123456', 'test')
        self.lock = threading.Lock()
        self.main()

    def main(self):
        threads = []
        for i in range(150):
            t = threading.Thread(target=self.insert_data)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def insert_data(self):
        db = self.db.get_instance()
        cursor = db.cursor()
        while True:
            if self.start_id >= self.max_id:
                break
            s = self.start_id
            with self.lock:
                self.start_id += 50
                if self.start_id > self.max_id:
                    self.start_id = self.max_id
            e = self.start_id
            for i in range(s, e):
                sql = 'insert into archives(`id`) values(%s)' % (i,)
                try:
                    cursor.execute(sql)
                    db.commit()
                    print(threading.current_thread().name, ': ', sql, ': success')
                except:
                    db.rollback()
                    print(threading.current_thread().name, ': ', sql, ':failed')
                    raise


if __name__ == '__main__':
    Test()
