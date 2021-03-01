import json
import random
import requests

# url = 'https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=491'

# headers = {
#     'User-Agent': 'jdskajdjjkjvd',
# }

# data_list = requests.get(url, headers=headers).json()

# with open('douban.txt', mode='a+', encoding='utf-8') as fp:
#     for data in data_list:
#         fp.write(data['title'] + '\n')


"""
豆瓣API
https://movie.douban.com/j/chart/top_list_count?type=8&interval_id=100%3A90

剧情： https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=20&limit=20
喜剧： https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=20&limit=20
动作： https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20
爱情： https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20


"""
# new_url = 'https://movie.douban.com/j/chart/top_list_count?type=8&interval_id=100%3A90'
# total= requests.get(new_url, headers=headers).json().get('total')
# print(total, type(total))  # 21 <class 'int'>


def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(10):
        ret += random.choice(string)
    return ret


data = []
for t in range(1, 32):
    for i in range(1, 11):
        id_str = '{}%3A{}'.format(i * 10, (i - 1) * 10)
        agent = random_str()
        headers = {
            'User-Agent': agent,
        }
        count_url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id={}'.format(t, id_str)
        try:
            total = requests.get(count_url, headers=headers).json().get('total')
            if total:
                agent = random_str()
                headers = {
                    'User-Agent': agent,
                }
                url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id={}&action=&start=0&limit={}'.format(t, id_str, total)
                movie_list = requests.get(url, headers=headers).json()
                for movie in movie_list:
                    for d in data:
                        if d['url'] == movie['url']:
                            break
                    else:
                        data.append(movie)
                print(url)
        except Exception:
            pass

new_data = [d for d in data if data.count(d) == 1]
print(len(new_data))
with open('doubanmovie7j.txt', mode='w', encoding='utf-8') as fp:
    json.dump(data, fp, ensure_ascii=False)


"""
Traceback (most recent call last):
  File "src\gevent\greenlet.py", line 766, in gevent._greenlet.Greenlet.run
  File "E:/Python_work/201910/20191017/day_work_1017/pa_donban_movie.py", line 9, in worker
    total = requests.get(count_url, headers=headers).json().get('total')
  File "D:\Programs\Python37\lib\site-packages\requests\models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "D:\Programs\Python37\lib\json\__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "D:\Programs\Python37\lib\json\decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "D:\Programs\Python37\lib\json\decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
2019-10-17T14:31:53Z <Greenlet at 0xb044378: worker('https://movie.douban.com/j/chart/top_list_count?t, 30, '100%3A90')> failed with JSONDecodeError

"""
