import json
import requests

# url = 'http://10.66.94.10:5000/'
url = 'http://10.66.94.10:5000/exe_cases/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36z",
}

with open('./task.json', mode='r', encoding='utf-8') as fp:
    data = json.load(fp)

print(f'{type(data)}\n{data}')

response = requests.post(url, json=data, headers=headers)
print(response.text)
