from pymongo import MongoClient
from weibospider.settings import MONGODB_URL, MONGODB_DATABASE

# Configure MongoClient with connection pooling
client = MongoClient(MONGODB_URL, maxPoolSize=50, waitQueueTimeoutMS=2000, connectTimeoutMS=2000)

db = client[MONGODB_DATABASE]
