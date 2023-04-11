import pymongo

from settings import MONGO_URI, MONGO_DATABASE


class JDspiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'JDspider':
            collection_name = 'jd_products'
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

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'JDcommentspider':
            collection_name = 'jd_comments'
            collection = self.db[collection_name]
            data = {
                'name': item['name'],
                'url': item['url'],
                'date': item['date'],
                'content': item['content']
            }
            collection.insert_one(data)
        return item
