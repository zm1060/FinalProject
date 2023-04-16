from pymongo import MongoClient

from jdspider.settings import MONGODB_DATABASE, MONGODB_URL

client = MongoClient(MONGODB_URL)

db = client[MONGODB_DATABASE]
