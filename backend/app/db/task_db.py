from pymongo import MongoClient
from weibospider.settings import MONGODB_URL

client = MongoClient(MONGODB_URL, maxPoolSize=50, waitQueueTimeoutMS=2000, connectTimeoutMS=2000)

task_db = client['users']
tasks_collection = task_db['tasks']
