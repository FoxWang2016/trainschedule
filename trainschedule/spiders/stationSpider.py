# -*- coding: utf-8 -*-
import scrapy


class StationspiderSpider(scrapy.Spider):
    name = 'stationSpider'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js']

    def parse(self, response):
        station_infos = response.text
        print(station_infos)
        station_info = station_infos.split("'")[1]
        print(station_info)
        station_Array = station_info.split("@")
        #for index, info in enumerate(station_Array, 1):
        for info in station_Array:
            for detail in info.split("|"):
                print(detail, end="    ")
            print("")
