import redis


if __name__ == '__main__':
    r = redis.Redis(host='127.0.0.1', port=6379)
    r.set('gender', 'male')
    r.set('start', '2019-10-26')
    r.set('good', int(True))