import json
import requests

url = 'https://www.tianqiapi.com/api/'
# url = 'https://www.tianqiapi.com/api/?version=v1&appid=13163115&appsecret=5qxu6KN1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36z",
}

data = {
    'version': 'v1',
    'appid': 13163115,
    'appsecret': '5qxu6KN1'
}

response = requests.get(url, params=data, headers=headers)

print(type(response))
print(response.json())

with open('tianqi.json', mode='w', encoding='utf-8') as fp:
    json.dump(response.json(), fp, ensure_ascii=False, indent=4)