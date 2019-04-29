
# -*- coding: utf-8 -*-
import json

import scrapy


class TrainnumberSpider(scrapy.Spider):
    name = 'trainNumber'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']

    def parse(self, response):
        train_number = response.text.split('=')[1].split()
        tr_json = json.load(train_number)
        print(tr_json)
