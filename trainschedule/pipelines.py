# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import ast

import redis
from scrapy.utils.project import get_project_settings
from elasticsearch import Elasticsearch


class TrainschedulePipeline(object):

    def __init__(self):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_password = settings.get('REDIS_PASSWORD')
        self.redis_db_num = settings.get('REDIS_DB_NUM')
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port
                                 , password=self.redis_password, db=self.redis_db_num)

        self.es_host = settings.get('ES_HOST')
        self.es = Elasticsearch(hosts=self.es_host, sniff_timeout=60)

    def process_item(self, item, spider):
        detailUrl = item.get("detailUrl")
        if(spider.name == 'trainNumber'):
            index = self.redis.sadd("12306_train:china_train_number_info_check", item)
            if index and "detailUrl" in item:
                h = self.redis.hset("12306_train:china_train_number_info", detailUrl, item)
                l = self.redis.lpush("12306_train:china_train_number_info_queue", detailUrl)
            return item
        else:
            train_info = str(self.redis.hget("12306_train:china_train_number_info", detailUrl), encoding="utf8")
            info = ast.literal_eval(train_info)
            info["details"] = item["details"]
            info.pop("detailUrl")
            self.es.index(index="train_time_table", body=info)
            return info
