# import random
# import requests
# from fake_useragent import UserAgent
#
# ua = UserAgent()
# url = 'https://www.baidu.com'
#
# headers = {
#     'useragent': ua.random,
# }
# # 先获取代理ip
# proxy_list = []
# for i in range(10):
#     res = requests.get('http://127.0.0.1:5555/random')
#     proxy_list.append(res.text)
# print(proxy_list)
# # print(random.choice(proxy_list))
#
#
# proxies = {
#     'http': 'http://{}'.format(random.choice(proxy_list)),
#     'https': 'https://{}'.format(random.choice(proxy_list)),
# }
#
# print(proxies)
# response = requests.request('get', url, proxies=proxies, headers=headers)
# with open('baidu.html', mode='wb') as fp:
#     fp.write(response.content)

"""
https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list
https://github.com/WiseDoge/ProxyPool
"""

import requests
import json
import pymongo
import pandas as pd

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['Per']

# url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
#
# response = requests.get(url)
#
# str_list = response.text.split('\n')
#
# for string in str_list:
#     if string.strip():
#         ret = json.loads(string.strip())
#         db['proxies'].insert_one(ret)
#
# print('ok')

ret = db['proxies'].find()

df = pd.DataFrame(data=ret)
print(df.head())
print(df.shape)

