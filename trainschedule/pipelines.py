# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.utils.project import get_project_settings


class TrainschedulePipeline(object):

    def __init__(self):
        settings = get_project_settings()
        self.redis_host = settings.get('REDIS_HOST')
        self.redis_port = settings.get('REDIS_PORT')
        self.redis_password = settings.get('REDIS_PASSWORD')
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port, password=self.redis_password)

    def process_item(self, item, spider):
        self.redis.sadd("china_train_station_info", item)
        return item
