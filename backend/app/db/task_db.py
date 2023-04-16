from pymongo import MongoClient
from weibospider.settings import MONGODB_URL

client = MongoClient(MONGODB_URL)

task_db = client['users']
tasks_collection = task_db['tasks']
