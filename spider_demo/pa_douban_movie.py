import json
import requests


url = 'https://m.douban.com/rexxar/api/v2/skynet/playlist/recommend/event_videos?count=30&out_skynet=true&for_mobile=1'

headers = {
    'Referer': 'https://m.douban.com/movie/beta',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}

response = requests.get(url, headers=headers)
# print(response.json())
with open('moviedou.json', mode='w', encoding='utf-8') as fp:
    json.dump(response.json(), fp, ensure_ascii=False, indent=4)