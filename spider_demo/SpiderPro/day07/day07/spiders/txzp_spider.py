# -*- coding: utf-8 -*-
import scrapy
import json
from day07.items import TengzhaoItem


class TxzpSpiderSpider(scrapy.Spider):
    name = 'txzp_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'day07.pipelines.TengPipeline': 300,}
    }
    allowed_domains = ['careers.tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1571819089536&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        ret = json.loads(response.text)
        # with open('tengxun.json', mode='w', encoding='utf-8') as fp:
        #     json.dump(ret, fp, ensure_ascii=False, indent=4)
        for data in ret['Data']['Posts']:
            post_url = 'http://careers.tencent.com/jobdesc.html?postId={}'.format(data['PostId'])
            detail_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1571820004830&postId={}'.format(data['PostId'])
            tz_item = TengzhaoItem()
            tz_item['title'] = data['RecruitPostName']
            tz_item['location'] = data['LocationName']
            tz_item['last_update_time'] = data['LastUpdateTime']
            tz_item['url'] = post_url
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, meta={'data': tz_item}, encoding='utf-8')
            # break

    def detail_parse(self, response):
        ret = json.loads(response.text)
        tz_item = response.meta['data']
        tz_item['requirement'] = ret['Data']['Requirement']
        tz_item['responsibility'] = ret['Data']['Responsibility']
        yield tz_item


        # with open('teng_detail.txt', mode='a', encoding='utf-8') as fp:
        #     fp.write(ret['Data']['RecruitPostName'] + '\n')

