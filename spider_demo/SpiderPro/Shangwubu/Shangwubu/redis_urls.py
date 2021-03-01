import redis
from Shangwubu.settings import REDIS_HOST, REDIS_PORT

r = redis.Redis(REDIS_HOST, REDIS_PORT)
for page in range(1, 101, 1):
    if page == 1:
        page = ''
    url = 'http://www.mofcom.gov.cn/article/ae/ai/?{}'.format(page)
    r.lpush('shangwubu:start_urls', url)