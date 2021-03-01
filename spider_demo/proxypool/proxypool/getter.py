from .db import RedisClient
from .crawler import Crawler
from .setting import POOL_UPPER_THRESHOLD
import sys


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_laber in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_laber]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()  # 缓冲区
                for proxy in proxies:
                    self.redis.add(proxy)
