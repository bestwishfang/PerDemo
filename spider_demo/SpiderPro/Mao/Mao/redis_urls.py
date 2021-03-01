# 该文件编写的程序： 主要是将任务加到redis数据库中

from redis import Redis
from Mao.settings import REDIS_HOST, REDIS_PORT

r = Redis(host=REDIS_HOST, port=REDIS_PORT)
for page in range(22):
    offset = page * 12
    task = 'https://maoyan.com/cinemas?offset={}'.format(offset)
    r.lpush('maoyan:start_urls', task)
    

