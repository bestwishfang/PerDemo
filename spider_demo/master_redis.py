from redis import Redis


r = Redis(host='10.10.14.245', port=6379, db=3)

for page in range(22):
    offset = page * 12
    task = 'https://maoyan.com/cinemas?offset={}'.format(offset)
    r.lpush('maoyan:start_urls', task)