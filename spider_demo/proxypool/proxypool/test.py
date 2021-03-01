import redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


class RedisClient():
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self, proxy, score=10):
        if not self.db.zscore(REDIS_KEY, proxy):
            print(1111)
            # return self.db.zadd(REDIS_KEY, score, proxy)
            mapping={proxy:score,}
            return self.db.zadd(REDIS_KEY, mapping)


if __name__ == '__main__':
    red=RedisClient()
    red.add('10.10.16.207:3000')

