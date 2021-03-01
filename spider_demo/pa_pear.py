import requests
from lxml import etree

url = 'https://www.pearvideo.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# content = requests.get(url, headers=headers).content.decode('utf-8')

with open('pear.html', mode='r', encoding='utf-8') as fp:
    content = fp.read()
tree = etree.HTML(content)
video_area = tree.xpath('//div[@id="vervideoTlist"]')[0]

data = []
video_big_info = {}
video_big = video_area.xpath('.//div[@class="vervideo-tlist-big"]')[0]

video_big_title = video_big.xpath('.//div[@class="vervideo-name"]/text()')[0].strip()
video_big_url = video_big.xpath('./div[@class="vervideo-tbd"]/a/@href')
video_big_url = url + video_big_url[0].strip()

# big_content = requests.get(video_big_url, headers=headers).content.decode('utf-8')
# with open('bigvideo.html', mode='w', encoding='utf-8') as fp:
#     fp.write(big_content)


print(video_big_title, video_big_url)


"""
https://www.pearvideo.com/video_1613542
https://video.pearvideo.com/mp4/adshort/20191018/cont-1613542-14497350_adpkg-ad_hd.mp4
"""