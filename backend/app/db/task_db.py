from pymongo import MongoClient
from weibospider.settings import MONGO_URI

client = MongoClient(MONGO_URI)

task_db = client['users']
