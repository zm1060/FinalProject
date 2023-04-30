import datetime
import logging

import pymongo

from jdspider.email_notifications import send_email


class JDspiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URL'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.task_db = self.client['users']

    def close_spider(self, spider):
        # 从爬虫对象中获取统计信息、task_id和user_id
        stats_info = spider.crawler.stats.get_stats()
        task_id = spider.task_id

        # 获取当前时间作为finish_time，并将其添加到stats_info字典中
        finish_time = datetime.datetime.now()
        stats_info['finish_time'] = finish_time

        # 将统计信息（包括task_id和user_id）写入MongoDB
        print(f"Stats info in pipeline: {stats_info}")
        self.task_db['tasks'].update_one({'task_id': task_id}, {'$set': {'stats': stats_info}}, upsert=True)
        self.client.close()
        subject = f"您的名称为{spider.name}的任务完成，任务号为 {task_id}!"
        body = f"数据收集任务完成，请前往您的任务中心进行下异步操作。  运行状态:{stats_info}"
        send_email(subject, body)

    def process_item(self, item, spider):
        if spider.name == 'JDspider':
            collection_name = str(spider.task_id)
            collection = self.db[collection_name]
            data = {
                'name': item['name'],
                'url': item['url'],
                'content': item['content']
            }
            collection.insert_one(data)
        return item


class JDcommentPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URL'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.task_db = self.client['users']

    def close_spider(self, spider):
        # 从爬虫对象中获取统计信息、task_id和user_id
        stats_info = spider.crawler.stats.get_stats()
        task_id = spider.task_id

        # 获取当前时间作为finish_time，并将其添加到stats_info字典中
        finish_time = datetime.datetime.now()
        stats_info['finish_time'] = finish_time

        # 将统计信息（包括task_id和user_id）写入MongoDB
        print(f"Stats info in pipeline: {stats_info}")
        self.task_db['tasks'].update_one({'task_id': task_id}, {'$set': {'stats': stats_info}}, upsert=True)
        self.client.close()
        subject = f"您的名称为{spider.name}的任务完成，任务号为 {task_id}!"
        body = f"数据收集任务完成，请前往您的任务中心进行下异步操作。  运行状态:{stats_info}"
        send_email(subject, body)

    def process_item(self, item, spider):
        if spider.name == 'JDcommentspider':
            collection_name = str(spider.task_id)
            collection = self.db[collection_name]
            data = {
                'name': item['name'],
                'url': item['url'],
                'date': item['date'],
                'content': item['content']
            }
            collection.insert_one(data)
        return item
