#!/usr/bin/env python
# encoding: utf-8
import datetime
import json
import os.path
import time
import pymongo
import logging

from celery import current_task


class JsonWriterPipeline(object):
    """
    写入json文件的pipline
    """

    def __init__(self):
        self.file = None
        if not os.path.exists('output'):
            os.mkdir('output')

    def process_item(self, item, spider):
        """
        处理item
        """
        if not self.file:
            now = datetime.datetime.now()
            file_name = spider.name + "_" + now.strftime("%Y%m%d%H%M%S") + '.jsonl'
            self.file = open(f'../output/{file_name}', 'wt', encoding='utf-8')
        item['crawl_time'] = int(time.time())
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item


class MongoDBPipeline(object):
    """
    存储数据到MongoDB的pipline
    """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        """
        连接到MongoDB数据库
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """
        关闭MongoDB数据库连接
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        处理item
        """
        collection_name = spider.name
        item['crawl_time'] = int(time.time())
        self.db[collection_name].insert_one(dict(item))
        return item

