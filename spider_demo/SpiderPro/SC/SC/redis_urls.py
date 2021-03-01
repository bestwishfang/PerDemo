import redis


r = redis.Redis(host='10.10.14.245', port=6379)
count = 0

with open(r'E:\Python_work\SpiderWork\SpiderPro\SC\city.txt', mode='r', encoding='utf-8') as fp:
    city_list = fp.readlines()

with open(r'E:\Python_work\SpiderWork\SpiderPro\SC\pinpai.txt', mode='r', encoding='utf-8') as fp:
    pinpai_list = fp.readlines()

city_list = list(set(city_list))
pinpai_list = list(set(pinpai_list))

for city in city_list:
    for pinpai in pinpai_list:
        url = 'https://{}.taoche.com{}'.format(city.strip(), pinpai.strip())
        r.lpush('taoche:start_urls', url)
        count += 1

r.set('count', count)