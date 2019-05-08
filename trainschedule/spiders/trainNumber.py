
# -*- coding: utf-8 -*-
import json
import ast

import scrapy


class TrainnumberSpider(scrapy.Spider):
    name = 'trainNumber'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']

    def parse(self, response):
        all_data = response.text.split('=')[1]
        data_json = json.loads(all_data)
        for date_key in data_json:
            train_number = data_json.get(date_key)
            for train_type in train_number:
                station_info = train_number.get(train_type)
                for train_code in station_info:
                    print(date_key, "   ", train_type, "   ", train_code.get("station_train_code"), "   "
                          , train_code.get("train_no"))
