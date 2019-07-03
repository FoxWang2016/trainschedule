# -*- coding: utf-8 -*-
import json

from scrapy_redis.spiders import RedisSpider

from trainschedule.items import TrainNumber


class TrainDetailsSpider(RedisSpider):
    name = 'trainDetails'
    # allowed_domains = ['kyfw.12306.cn']
    # start_urls = ['http://kyfw.12306.cn/']
    redis_key = '12306_train:china_train_number_info_queue'

    def parse(self, response):
        result = json.loads(response.text)
        if result.get("status"):
            trainNumber = TrainNumber()
            trainNumber["details"] = result.get("data").get("data")
            trainNumber["detailUrl"] = response.url
            yield trainNumber

