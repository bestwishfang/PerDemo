import time
import math
import pymongo
import requests
import hashlib
from fake_useragent import UserAgent


class PaTouTiao(object):
    def __init__(self, mid, user_agent):
        self.mid = mid
        self.url = 'https://www.toutiao.com/c/user/article/'
        self.headers = {
            'referer': 'https://www.toutiao.com/c/user/{}'.format(self.mid),
            'user-agent': user_agent,
        }
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['TouTiaoNews']

    # 构建请求数据
    def create_data(self, max_behot_time):
        md5 = hashlib.md5()
        e = math.floor(time.time())
        i = hex(e)[2:].upper()
        md5.update(str(e).encode('utf-8'))
        ret = md5.hexdigest()
        t = ret.upper()
        o = t[0:5]
        n = t[-5:]
        a = ''
        for s in range(5):
            a += o[s] + i[s]

        r = ''
        for l in range(5):
            r += i[l + 3] + n[l]

        data = {
            'page_type': 1,
            'user_id': self.mid,
            'max_behot_time': max_behot_time,
            'count': 20,
            'as': 'A1' + a + i[-3:],
            'cp': i[0:3] + r + 'E1',
            '_signature': '1uOraRARi2EThvPkAv1vPtbjq3',  # _signature 好厉害 只能用于新华网头条号
        }
        return data

    # 请求数据
    def get_response(self, max_behot_time):
        data = self.create_data(max_behot_time)
        response = requests.get(self.url, params=data, headers=self.headers)
        ret = response.json()
        max_behot_time = ret['next']['max_behot_time']  # 下次请求的max_behot_time
        news_list = ret['data']  # news_list  <class 'list'>
        return max_behot_time, news_list

    # 保存文件
    def save_file(self, n, news_list):
        for news in news_list:
            self.db['xinhua'].insert_one(news)
        print("第{}页新闻保存成功".format(n))


if __name__ == '__main__':
    user_agent = UserAgent()
    mid = 4377795668  # 新华网头条号
    patiao = PaTouTiao(mid, user_agent.random)
    # 爬取前十页新闻
    max_behot_time = 0
    for i in range(10):
        max_behot_time, news_list = patiao.get_response(max_behot_time)
        patiao.save_file(i + 1, news_list)

"""
page_type: 1
user_id: 4377795668
max_behot_time: 0
count: 20
as: A1652D5B5BF77CE
cp: 5DBB37970C6E3E1
_signature: eMm5vRAXJXW9rOEwX0M2KXjJua
"""
