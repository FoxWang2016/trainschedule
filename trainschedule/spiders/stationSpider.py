# -*- coding: utf-8 -*-
import redis
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy import cmdline
from trainschedule.items import StationItem


class StationspiderSpider(scrapy.Spider):
    name = 'stationSpider'
    allowed_domains = ['kyfw.12306.cn']
    #start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js']
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9104']

    def __init__(self):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_password = settings.get('REDIS_PASSWORD')
        self.redis_db_num = settings.get('REDIS_DB_NUM')
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port
                                 , password=self.redis_password, db=self.redis_db_num)

    def parse(self, response):
        station_infos = response.text
        print(station_infos)
        station_info = station_infos.split("'")[1]
        print(station_info)
        station_Array = station_info.split("@")
        #for index, info in enumerate(station_Array, 1):
        index_info = ""
        try:
            for info in station_Array:
                index_info = info
                item = StationItem()
                keyList = ("pingyinma", "stationName", "telegraphCode", "pingyin", "acronym", "id")
                i = 0
                for detail in info.split("|"):
                    item[keyList[i]] = detail
                    i = i+1
                    print(detail, end="    ")
                print("")
                if info != '':
                    self.redis.hset("china_train_station_info", item["stationName"], item)
                    self.redis.hset("china_train_station_telegraph_code", item["stationName"], item["telegraphCode"])
        except:
            print("ERROR:", index_info)

    # def close(spider, reason):
    #     cmdline.execute("scrapy crawl trainNumber".split())
