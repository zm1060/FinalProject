from pymongo import MongoClient
from jdspider.settings import MONGO_URI, MONGO_DATABASE

client = MongoClient(MONGO_URI)

db = client[MONGO_DATABASE]
