#!/usr/bin/env python
# encoding: utf-8
import datetime
import time
import pymongo
import logging

from weibospider.email_notifications import send_email


class MongoDBPipeline(object):
    """
    存储数据到MongoDB的pipline
    """

    def __init__(self, mongo_uri, mongo_db):
        self.db = None
        self.client = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.task_db = mongo_db

        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URL'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        """
        连接到MongoDB数据库
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.task_db = self.client['users']

    def close_spider(self, spider):
        """
        关闭MongoDB数据库连接
        """
        # 从爬虫对象中获取统计信息、task_id和user_id
        stats_info = spider.crawler.stats.get_stats()
        task_id = spider.task_id
        # 获取当前时间作为finish_time，并将其添加到stats_info字典中
        finish_time = datetime.datetime.now()
        stats_info['finish_time'] = finish_time

        # 将统计信息（包括task_id和user_id）写入MongoDB
        print(f"Stats info in pipeline: {stats_info}")
        self.task_db['tasks'].update_one(
            {'task_id': task_id},
            {'$set': {'status': 'finished', 'stats': stats_info}}
        )
        self.client.close()
        subject = f"您的名称为{spider.name}的任务完成，任务号为 {task_id}!"
        body = f"数据收集任务完成，请前往您的任务中心进行下一步操作。 可以前往https://scrapeops.io/app/dashboard   查看数据收集程序的状态. 运行状态:{stats_info}"
        send_email(subject, body)

    def process_item(self, item, spider):
        """
        处理item
        """
        collection_name = str(spider.task_id)
        item['crawl_time'] = int(time.time())
        self.db[collection_name].insert_one(dict(item))
        return item

