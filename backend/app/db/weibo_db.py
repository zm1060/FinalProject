from pymongo import MongoClient
from weibospider.settings import MONGODB_URL, MONGODB_DATABASE
client = MongoClient(MONGODB_URL)

db = client[MONGODB_DATABASE]