import requests
import json


url = 'https://dc.3.cn/category/get'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

response = requests.get(url, headers=headers)

with open('jd.json', mode='w', encoding='utf-8') as fp:
    json.dump(response.json(), fp, ensure_ascii=False, indent=4)
