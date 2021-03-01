# -*- coding: utf-8 -*-
import re
import json
import scrapy
from Patengxun.items import PatengxunItem


class TengxunspiderSpider(scrapy.Spider):
    name = 'tengxunspider'
    custom_settings = {
        'ITEM_PIPELINES': {'Patengxun.pipelines.PatengxunPipeline': 300,}
    }
    allowed_domains = ['pacaio.match.qq.com']
    start_urls = []
    mid_dict = {
        '央视新闻': 58,
        '中国新闻网': 1124,
        '中国周刊': 1156,
        '央视网新闻': 5278151,
        '人民网': 1456,
        '新华社新闻': 10859191,
        '北青Qnews': 16314728,
        '环球网': 26082,
        '新京报': 26134,
        '观察者网': 5006122,
    }
    for mid in mid_dict.values():
        for page in range(10):
            url = 'https://pacaio.match.qq.com/om/mediaArticles?mid={}&num=30&page={}'.format(mid, page)
            start_urls.append(url)

    def parse(self, response):
        ret = response.text
        ret_dict = json.loads(ret, encoding='utf-8')
        # print(type(ret_dict)) # dict
        # with open('newyangshi.json', mode='w', encoding='utf-8') as fp:
        #     json.dump(ret_dict, fp, ensure_ascii=False, indent=4)
        # print(type(ret))  # atr
        # with open('yanshi.json', mode='w', encoding='utf-8') as fp:
        #     fp.write(ret)
        tengxun_item = PatengxunItem()
        for news in ret_dict['data']:
            news_url = news['url']
            tengxun_item['title'] = news['title']
            tengxun_item['source'] = news['source']
            tengxun_item['url'] = news_url
            tengxun_item['engineer'] = 'fang'

            print(news_url)
            yield scrapy.Request(url=news_url, callback=self.parse_detail, meta={'data': tengxun_item},
                                 encoding='utf-8', dont_filter=True)

    def parse_detail(self, response):

        # with open('unknown.html', mode='w', encoding='utf-8') as fp:
        #     fp.write(response.text)
        news_ret = response.text
        pattern = re.compile(r'content: (\{.*?)id:', re.S)
        news_str = pattern.findall(news_ret)[0].strip()
        news_str = news_str.rsplit(',', 1)[0]
        news_dict = json.loads(news_str, encoding='utf-8')
        news_content = news_dict['cnt_html']
        news_content = re.sub(r'\<(.*?)\>', '', news_content)
        news_content = news_content.rsplit('▌', 1)[0]
        # print(type(news_content), news_content)
        alt_time = news_dict['alt_time']
        tengxun_item = response.meta['data']
        tengxun_item['release_time'] = alt_time
        tengxun_item['content'] = news_content

        yield tengxun_item

        # with open('hnewsstr.json', mode='w', encoding='utf-8') as fp:
        #     json.dump(news_dict, fp, ensure_ascii=False, indent=4)
        # print(news_str)
