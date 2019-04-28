# -*- coding: utf-8 -*-
import scrapy


class StationspiderSpider(scrapy.Spider):
    name = 'stationSpider'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['http://kyfw.12306.cn/']

    def parse(self, response):
        pass
