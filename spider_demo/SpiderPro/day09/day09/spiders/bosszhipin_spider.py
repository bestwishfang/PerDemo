# -*- coding: utf-8 -*-
import scrapy


class BossSpiderSpider(scrapy.Spider):
    name = 'bosszhipin_spider'
    custom_settings = {
        # 'ITEM_PIPELINES': {'day09.pipelines.BossJobPipeline': 300,},
        'DOWNLOADER_MIDDLEWARES': {'day09.myMW.BossDownloaderMiddleware': 543,},
    }
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python']

    def parse(self, response):
        with open('bpython.html', mode='w', encoding='utf-8') as fp:
            fp.write(response.text)

