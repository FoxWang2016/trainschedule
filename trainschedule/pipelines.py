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
        self.es = Elasticsearch(hosts=self.es_host, sniff_on_start=True, sniff_timeout=60)
        mappings = {
            "mappings": {
                "type_doc_test": {  # type_doc_test为doc_type
                    "properties": {
                        "id": {
                            "type": "long",
                            "index": "false"
                        },
                        "serial": {
                            "type": "keyword",  # keyword不会进行分词,text会分词
                            "index": "false"  # 不建索引
                        },
                        "tags": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "keyword", "index": True},
                                "dominant_color_name": {"type": "keyword", "index": True},
                                "skill": {"type": "keyword", "index": True},
                            }
                        },
                        "hasTag": {
                            "type": "long",
                            "index": True
                        },
                        "status": {
                            "type": "long",
                            "index": True
                        },
                        "createTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                        },
                        "updateTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                        }
                    }
                }
            }
        }

        self.es.indices.create(index='train_time_table', body=mappings)

    def process_item(self, item, spider):
        if(spider.name == 'trainNumber'):
            index = self.redis.sadd("12306_train:china_train_number_info_check", item)
            if index:
                self.redis.lpush("12306_train:china_train_number_info_queue", item['detailUrl'])
                self.redis.hset("12306_train:china_train_number_info", item['detailUrl'], item)
                return item
        else:
            train_info = str(self.redis.hget("12306_train:china_train_number_info", item['detailUrl']), encoding="utf8")
            info = ast.literal_eval(train_info)
            info["details"] = item["details"]
            self.es.index(index="train_time_table", body=info)
            return info
