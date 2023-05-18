from pymongo import MongoClient

from jdspider.settings import MONGODB_DATABASE, MONGODB_URL

client = MongoClient(MONGODB_URL, maxPoolSize=50, waitQueueTimeoutMS=2000, connectTimeoutMS=2000)

db = client[MONGODB_DATABASE]
