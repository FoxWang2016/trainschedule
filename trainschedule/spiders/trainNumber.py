
# -*- coding: utf-8 -*-
import json
import ast

import redis
import scrapy
from scrapy.utils.project import get_project_settings

from trainschedule.items import TrainNumber


class TrainnumberSpider(scrapy.Spider):
    name = 'trainNumber'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']

    def __init__(self):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_password = settings.get('REDIS_PASSWORD')
        self.redis_db_num = settings.get('REDIS_DB_NUM')
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port
                                 , password=self.redis_password, db=self.redis_db_num)

    def parse(self, response):
        all_data = response.text.split('=')[1]
        data_json = json.loads(all_data)
        for date_key in data_json:
            train_number = data_json.get(date_key)
            for train_type in train_number:
                station_info = train_number.get(train_type)
                for train_code in station_info:
                    station_train_code = train_code.get("station_train_code")
                    start_station = ""
                    end_station = ""
                    number = ""
                    if (station_train_code.find("(")):
                        number = station_train_code.split("(")[0]
                        stations = station_train_code.split("(")[1]
                        start_station = stations.split("-")[0]
                        end_station = stations.split("-")[1][:-1]
                        trainNumber = TrainNumber()
                        trainNumber.startDate = date_key
                        trainNumber.trainType = train_type
                        trainNumber.trainNumber = number
                        trainNumber.departureStation = start_station
                        trainNumber.departureAcronym = str(self.redis.hget("china_train_station_telegraph_code"
                                                                           , start_station), encoding="utf8")
                        trainNumber.terminus = end_station
                        trainNumber.terminusAcronym = str(self.redis.hget("china_train_station_telegraph_code"
                                                                          , end_station), encoding="utf8")
                        trainNumber.trainCode = train_code.get("train_no")
                        yield trainNumber

                    print(date_key, "   ", train_type, "   ", number, "   ", start_station, "   "
                          , str(self.redis.hget("china_train_station_telegraph_code", start_station), encoding="utf8")
                          , "   ", end_station, "   "
                          , str(self.redis.hget("china_train_station_telegraph_code", end_station), encoding="utf8")
                          , "   ", train_code.get("train_no"))
