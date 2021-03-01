import requests
import pymongo
from fake_useragent import UserAgent


class PaJiQiZhiXin(object):
    # 爬取知乎机器之心 文章

    def __init__(self, url, user_agent):
        self.count = 1  # 用于计算多少页
        self.num = 0
        self.url = url
        self.user_agent = user_agent
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['JiQiZhiXin']

    def get_response(self):
        headers = {
            'user-agent': self.user_agent.random,
        }
        response = requests.get(self.url, headers=headers)
        return response.json()

    # 保存文件
    def save_file(self, news_list):
        for news in news_list:
            self.db['news'].insert_one(news)
            self.num += 1
        print("第{}页新闻保存成功".format(self.count))

    def process_response(self):
        ret = self.get_response()
        print(ret['paging']['is_end'])
        if not ret['paging']['is_end']:
            self.url = ret['paging']['next']
            news_list = ret['data']
            self.save_file(news_list)
            self.count += 1
            self.process_response()


if __name__ == '__main__':
    user_agent = UserAgent()
    url = 'https://www.zhihu.com/api/v4/members/ji-qi-zhi-xin-65/activities'
    jiqi = PaJiQiZhiXin(url, user_agent)
    print('Spider starting ...')
    jiqi.process_response()
    print("总共{}篇文章".format(jiqi.num))

